"""
Command line interface for pushing data into TOG

Usage:
  tog push --client-id=<client-id> --lang=<lang> --days=<days> --job-id=<job-id> \
[--data_source=<data_source>] [--priority=<priority>]
  tog filepush --file=<file-path> --job-id=<job-id> [--data_source=<data_source>] [--priority=<priority>]
  tog (-h|--help)

Options:
    --client-id=<client-id>         Client ID of the data to be downloaded
    --lang<lang>                    Language code (en,hi)
    --days=<days>                   Number of days prior to today, from which data is to be downloaded
    --job-id=<job-id>               TOG job id into which data will be pushed
    --file=<file-path>              Json input file to be pushed, must be the same format as the fsm-pull schema
    --data_source=<data_source>     Data source where data is coming [default: fsm]
    --priority=<priority>           Priority order of data [default: 1]

    Filters are not available in cli
"""


import os
import json
import requests
import urllib
from typing import Any, List

import pandas as pd
from tqdm import tqdm
from docopt import docopt

from togpush import fsm
from togpush.data_filters import check_data_format, extract_only_user, filter_data
from togpush.utils import chunk_list


def initialize_connection(job_id: int):
    """
    Function to initialize the connection to the Database
    :param job_id: TOG job id, where data is to be uploaded
    :return: headers: Authentication Details
             task_url: Upload URL
    """
    credential = {"email": os.environ["API_MAIL"],
                  "password": os.environ["API_PASS"]}

    access_token = requests.post(os.environ["AUTH_URL"], data=json.dumps(credential)).json()["access_token"]

    headers = {"Authorization": os.environ["AUTH_NAME"] + str(access_token)}
    task_url = os.environ["TOG_JOB_URL"] + str(job_id)

    return headers, task_url


def tog_filter(entry: dict):
    """
    Function which adds filters to be used by tog for filtering datasets,
    currently only predicted intent, state and predicted slots are added
    :param entry: User conversation turn
    :return: filter_dict filter dictionary based on user turn
    """
    filter_dict = {"current_state": entry["state"]}

    if entry["prediction"] and "intents" in entry["prediction"]:

        output_intent = entry["prediction"]["intents"]

        try:
            filter_dict["predicted_intent"] = output_intent[0]["ML_MODEL_PREDICTION"]
        except KeyError:
            filter_dict["predicted_intent"] = output_intent[0]["name"]

        if "entities" in output_intent[0] and output_intent[0]["entities"]:
            filter_dict["acknowledged_slots"] = [temp_entry["name"] for temp_entry in output_intent[0]["entities"]]
        elif "slots" in output_intent[0] and output_intent[0]["slots"]:
            filter_dict["acknowledged_slots"] = [temp_entry["name"] for temp_entry in output_intent[0]["slots"]]

    return filter_dict


def convert_to_tog(dataset: list, data_source: str, priority: int):
    """
    TOG DB has a different format from FSM DB, this function converts FSM format to TOG.
    :param dataset: FSM format dataset
    :param data_source: Source of data (Generally FSM)
    :param priority: Priority of tagging (Generally 1)
    :return: tog_dataset: TOG format dataset
    """
    tog_dataset = []

    for entry in dataset:
        if "conversation_uuid" in entry:
            temp_id = entry["conversation_uuid"]
        elif "conversation_id" in entry:
            temp_id = entry["conversation_id"]
        else:
            raise NotImplementedError

        entry["filter"] = tog_filter(entry)

        tog_dataset.append({"priority": priority,
                            "data_source": data_source,
                            "data_id": str(temp_id),
                            "data": entry,
                            "is_gold": False})

    return tog_dataset


def upload_data(dataset: list, job_id: int):
    """
    Function to upload the TOG format dataset to a given TOG job id
    :param dataset:
    :param job_id:
    :return: None
    """
    headers, url = initialize_connection(job_id)

    total_pushed = 0

    print(f"Pushing {len(dataset)} data points to Job ID: {job_id}")

    for index in tqdm(range(0, len(dataset), 20)):

        resp = requests.post(url=url, headers=headers, json=dataset[index: index+20])

        if resp.status_code not in [200, 201]:
            print(resp.status_code, resp.text)
        else:
            total_pushed += 20

    if total_pushed < len(dataset):

        resp = requests.post(url=url, headers=headers, json=dataset[total_pushed:])

        if resp.status_code not in [200, 201]:
            print(f"Only pushed {total_pushed} data points to Job Id: {job_id}")

            raise Exception(str(resp.status_code) + str(resp.text))
        else:
            total_pushed += len(dataset) - total_pushed

    print(f"Successfully pushed {total_pushed} data points to Job Id: {job_id}")


def push(client_id: int, lang: str, days: int, job_id: int, data_source="FSM", priority=1, **filter_type):
    """
    Function to pull data from FSM Database and push it to TOG DB.
    :param client_id: FSM based Client ID of the dataset to be pushed.
    :param lang: Language code of the dataset.
    :param days: Number of days for which data needs to be pushed,
                    ex: 0 for current day, 1 for current + previous day and so on.
    :param job_id: TOG Job ID, where data to be pushed.
    :param data_source: Source of data, Default: FSM
    :param priority: Priority for data for Tagging, Default: 1
    :param filter_type: Keyword argument for data filter, please check documentation for supported filters
    :return: None
    """
    fsm_dataset = fsm.pull(client_id, lang, days)

    if fsm_dataset:
        user_dataset = extract_only_user(fsm_dataset)

        filtered_dataset = filter_data(user_dataset, **filter_type)

        tog_dataset = convert_to_tog(filtered_dataset, data_source, priority)

        upload_data(tog_dataset, job_id)
    else:
        raise RuntimeError("Found zero data points, please check/change your input attributes")


def filepush(file: str, job_id: int, data_source="FSM", priority=1, **filter_type):
    """
    Function to upload FSM format dataset from a file to the given TOG Job ID
    :param file: Json File path containing FSM-format dataset
    :param job_id: TOG Job ID
    :param data_source: Source of dataset, Default: FSM
    :param priority: Priority for data for Tagging, Default: 1
    :param filter_type: Keyword argument for data filter, please check documentation for supported filters
    :return: Null
    """
    if os.path.exists(file):
        fsm_dataset = json.load(open(file))
    else:
        raise FileNotFoundError(f"{file} File doesn't exists")

    if fsm_dataset:
        user_dataset = extract_only_user(fsm_dataset)

        if check_data_format(user_dataset):

            filtered_dataset = filter_data(user_dataset, **filter_type)

            tog_dataset = convert_to_tog(filtered_dataset, data_source, priority)

            upload_data(tog_dataset, job_id)
        else:
            raise RuntimeError("Data format is not as per the fsm pull Schema, please check")
    else:
        raise RuntimeError("Found zero data points, please check/change your input attributes")

def upload_data_v2(dataset_chunks: List[List[Any]], job_id: int, access_token: str):
    """
    Upload datasets to tog task.

    :param dataset_chunks: [description]
    :type dataset_chunks: List[List[Any]]
    :param job_id: [description]
    :type job_id: int
    :param access_token: [description]
    :type access_token: str
    :return: [description]
    :rtype: [type]
    """
    headers = {"Authorization": f"Bearer {access_token}"}

    task_url = f"{os.environ['TOG_JOB_URL']}{job_id}"
    print(task_url)
    errors = []
    for dataset in dataset_chunks:
        response = requests.post(url=task_url, headers=headers, json=dataset)
        if response.status_code > 201:
            errors.append({"cause": response.text})
    return errors


def push_csv2tog(job_id: int, file_path: str, access_token: str):
    """
    Push an untagged csv from a given path to tog.

    :param job_id: Tog job id where data should be pushed.
    :type job_id: int
    :param file_path: Untagged dataset path.
    :type file_path: str
    """
    data_frame = pd.read_csv(file_path)
    dataset = []
    expected_columns = ["call_uuid", "conversation_uuid", "alternatives", 
        "audio_url", "reftime", "prediction", "state", "ack_slots", "end_state", 
        "call_duration", "state_transitions"]

    for _, row in tqdm(data_frame.iterrows(), total=len(data_frame)):
        safe_row = {col: row[col] if not pd.isna(row[col]) else json.dumps([]) for col in data_frame.columns}

        alternatives = json.loads(safe_row["alternatives"])
        if alternatives and isinstance(alternatives, list) and isinstance(alternatives[0], dict):
            alternatives = [alternatives]
 
        dataset.append({
            "priority": 1,
            "data_source": "fsm",
            "data_id": safe_row["conversation_uuid"],
            "data": {
                "call_uuid": safe_row["call_uuid"],
                "conversation_uuid": safe_row["conversation_uuid"],
                "alternatives": alternatives,
                "audio_url": safe_row["audio_url"],
                "reftime": safe_row["reftime"],
                "prediction": safe_row["prediction"],
                "state": safe_row["state"],
                "ack_slots": safe_row["ack_slots"],
                "end_state": safe_row["end_state"],
                "call_duration": safe_row["call_duration"],
                "state_transitions": safe_row["state_transitions"]
            },
            "is_gold": False
        })

    dataset_chunks = chunk_list(dataset, chunks=20)
    return upload_data_v2(dataset_chunks, job_id, access_token)


def push_v2(file_path: str, job_id: int, access_token: str):
    """
    Push an untagged dataset to tog.

    :param file_path: Untagged dataset path.
    :type file_path: str
    :param job_id: Tog job id where data should be pushed.
    :type job_id: int
    """
    _, extension = os.path.splitext(file_path)
    if extension != ".csv":
        raise ValueError("Expected file extension to be a csv.")
    return push_csv2tog(job_id, file_path, access_token)


def main():
    """
    Function for CLI access, will be deprecated in the following versions
    """
    args = docopt(__doc__)

    if args["push"]:

        push(args["--client-id"], args["--lang"], args["--days"], args["--job-id"],
             data_source=args["--data_source"] or "FSM", priority=args["--priority"] or 1)

    elif args["filepush"]:

        filepush(args["--file"], args["--job-id"],
                 data_source=args["--data_source"] or "FSM", priority=args["--priority"] or 1)

    else:
        raise RuntimeError("Please enter a valid argument, \n currently only push and file-push are supported")
