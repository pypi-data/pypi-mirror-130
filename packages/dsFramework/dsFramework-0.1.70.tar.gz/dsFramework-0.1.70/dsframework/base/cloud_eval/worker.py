import json
import logging
import sys

from logdecorator import log_on_start, log_on_end, log_on_error, log_exception

import csv
from typing import Dict, List

import io
import boto3
import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry


service_client = None

endpoint_name = None


@log_on_start(logging.INFO, "loading dataset {input_path:s}...")
@log_on_error(logging.ERROR, "Error on loading dataset {input_path:s}: {e!r}",
              on_exceptions=IOError,
              reraise=True)
@log_on_end(logging.INFO, "Downloading {input_path:s} finished successfully")
def load_csv(input_path):
    with download_file_from_s3(input_path) as csvfile:
    # with open(input_path, newline='') as csvfile:
        input_reader = csv.DictReader(csvfile, delimiter=',')
        rows = [row for row in input_reader]
        return rows


@log_on_start(logging.DEBUG, "invoke_model on {row}...")
def invoke_model(row):
    request_payload = service_client.get_request_payload(row)
    headers = service_client.get_request_headers(row)

    target_host = "127.0.0.1"
    target_port = 8080
    url = f"http://{target_host}:{target_port}/{endpoint_name}"

    retries = Retry(total=5, backoff_factor=1, read=5, status=5,  # allowed_methods=['GET', 'POST'],
                    status_forcelist=[502, 503, 504, 400])
    s = requests.Session()
    s.mount('http://', HTTPAdapter(max_retries=retries))

    try:
        response = s.post(
            url=url,
            json=request_payload,
            headers=headers
        )
    except requests.ConnectionError as ce:
        raise Exception(
            f"Error connecting to service at {url}. Is the service up and running, with the correct port?") from ce
    except Exception as e:
        raise Exception(f"Error call service") from e

    response_json = response.json()
    if "error" in response_json:
        raise Exception("Error in model service")

    model_prediction = service_client.extract_model_predictions_from_response(response_json)

    return model_prediction


@log_on_start(logging.INFO, "Starting work on dataset...")
@log_on_error(logging.ERROR, "Error invoking model on dataset: {e!r}",
              on_exceptions=IOError,
              reraise=True)
@log_on_end(logging.INFO, "Completed working on dataset")
def work_on(rows):
    for row in rows:
        # Call model and get prediction
        row['prediction'] = json.dumps(invoke_model(row))
        # Run evaluation and get confusion matrix
        row['evaluation'] = service_client.evaluate_model_results(row)
        # Format the output structure
        service_client.set_format_output(row)
    return rows


def write_to_s3(csv_content, bucket_name, file_path):
    client = boto3.client('s3')
    response = client.put_object(
        Body=csv_content,
        Bucket=bucket_name,
        Key=file_path
    )


@log_on_start(logging.INFO, "writing dataset {output_path:s}...")
@log_on_error(logging.ERROR, "Error on write dataset {output_path:s}: {e!r}",
              on_exceptions=IOError,
              reraise=True)
@log_on_end(logging.INFO, "Writing {output_path:s} finished successfully")
def write_output(output: List[Dict], output_path):
    bucket_name, file_path = parse_s3_url(output_path)
    with io.StringIO() as csvfile:
    # with open(output_path, 'w', newline='') as csvfile:
        fieldnames = list(output[0].keys())
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quotechar='"')

        writer.writeheader()
        for row in output:
            writer.writerow(row)

        csv_content = bytes(csvfile.getvalue(), encoding='utf-8')

        write_to_s3(csv_content, bucket_name, file_path)


def main(input_path: str, output_path: str):
    # Load CSV
    rows = load_csv(input_path)
    # Call model and evaluate on each row
    output = work_on(rows)
    # Write output file
    write_output(output, output_path)


def download_file_from_s3(source_s3_url: str):
    bucket_name, filepath = parse_s3_url(source_s3_url)
    s3 = boto3.client('s3', region_name='us-east-2')
    res = s3.get_object(Bucket=bucket_name, Key=filepath)['Body'].read()
    file_stream = io.StringIO(res.decode('utf-8'))
    return file_stream


def parse_s3_url(s3_url: str):
    bucket_name, filepath = s3_url.split('//')[1].split('/', maxsplit=1)
    return bucket_name, filepath


# if __name__ == '__main__':
#     # input = "./test/dummy_dataset.csv"
#     input = "s3://noamm-test-batch-bucket/datasets/dummy_dataset.csv"
#     # output = "./test/dummy_output.csv"
#     output = "s3://noamm-test-batch-bucket/predictions/dummy_output.csv"
#     main(input, output)

if __name__ == '__main__':
    from cloud_eval.cloud_eval_client import CloudEvalClient

    input_dataset_filename, output_dataset_filename = sys.argv[1:1 + 2]
    service_client = CloudEvalClient()
    endpoint_name = service_client.get_endpoint_name()
    main(input_dataset_filename, output_dataset_filename)
