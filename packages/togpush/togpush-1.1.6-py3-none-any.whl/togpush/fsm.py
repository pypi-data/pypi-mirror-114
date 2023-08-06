"""
Code for downloading data from fsm data server.
All the turns from a call is downloaded.

Usage:
  fsm pull --client-id=<client-id> --lang=<lang> --days=<days> --output-json=<output-json>
  [--call-quantity=<call_quantity>]

Options:
    --client-id=<client-id>             Client ID of the data to be downloaded
    --lang=<lang>                       Language code (en,hi)
    --days=<days>                       Number of Days prior to today, from which data is to be downloaded
    --output-json=<output-json>         Output json file name
    --call-quantity=<call_quantity>     Number of random calls to be returned or saved
"""

import os
import json
import psycopg2
import datetime

from docopt import docopt
from typing import Dict, List, Optional

from togpush import __version__
from togpush.data_filters import filter_data


def initialize_db_connection():
    """
    Function to initialize the connection to the Database, refer to Readme for ENV Variables to be set
    """
    if os.getenv("DB_PASS") is None:
        raise ValueError("Credentials are not set. Check for missing environment variables.")

    return psycopg2.connect(host=os.getenv("DB_HOST"), database=os.getenv("DB_NAME"),
                            user=os.getenv("DB_USER"), password=os.getenv("DB_PASS"),
                            port=os.getenv("DB_PORT"))


def download_data(client_id: int, lang: str, days: int) -> List[Dict]:
    """
    Function to download data from FSM Database
    :param client_id: FSM based Client ID of the dataset to be pushed.
    :param lang: Language code of the dataset.
    :param days: Number of days for which data needs to be pushed,
                    ex: 0 for current day, 1 for current + previous day and so on.
    :return: fsm_dataset: Downloaded Dataset
    """
    start_date = (datetime.datetime.now() - datetime.timedelta(days=int(days))).strftime("%Y-%m-%d")
    end_date = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")

    print(f"Downloading Data created between {start_date} 00:00:00 and {end_date} 00:00:00")

    connection = initialize_db_connection()

    with connection.cursor() as cur:
        cur.execute(
            f"with call_contexts as (with calls as\
            (SELECT calls.id, calls.client_id FROM calls\
            WHERE calls.client_id={client_id}\
            AND calls.created_at>'{start_date}'\
            AND calls.created_at<'{end_date}')\
            SELECT call_contexts.call_id, call_contexts.language_code\
            from call_contexts JOIN calls on calls.id = call_contexts.call_id\
            WHERE call_contexts.language_code in ('{lang}'))\
            SELECT conversations.call_id , conversations.id as conversation_id,\
            conversations.text, conversations.state, conversations.created_at as reftime,\
            conversations.audio_base_path || conversations.audio_path as audio_url,\
            conversations.prediction, conversations.debug_metadata, \
            conversations.metadata, conversations.type, conversations.sub_type FROM conversations\
            JOIN call_contexts on call_contexts.call_id = conversations.call_id\
            ORDER BY conversations.call_id desc, conversations.id asc"
        )
        field_names = [i[0] for i in cur.description]
        fsm_dataset = [{description: value for description, value in zip(field_names, row)} for row in cur.fetchall()]
        print(f"Total downloaded entries: {len(fsm_dataset)}")

    for row in fsm_dataset:

        row["audio_url"] = row["audio_url"]\
            .replace("https://s3.ap-south-1.amazonaws.com/hermes-cca",
                     "https://hermes-cca.s3.ap-south-1.amazonaws.com")\
            .replace("%2F", "/")

        if row["debug_metadata"] and "plute_request" in row["debug_metadata"]:
            temp_alternatives = row["debug_metadata"]["plute_request"]["alternatives"]

            if temp_alternatives:
                row["alternatives"] = [temp_alternatives] if isinstance(temp_alternatives[0], dict) \
                    else temp_alternatives
            else:
                row["alternatives"] = [[]]

        elif row["prediction"] and "graph" in row["prediction"]:
            row["alternatives"] = row["prediction"]["graph"]["input"][0]
        else:
            row["alternatives"] = [[]]

        # Converting reftime from psycopg2 datetime format to string
        row["reftime"] = row["reftime"].strftime("%Y-%m-%dT%H:%M:%SZ")

    return fsm_dataset


def pull(client_id: int, lang: str, days: int, output_file: Optional[str] = "", call_quantity: Optional[int] = 0):
    """
    Function to pull and save/return from FSM Database
    :param client_id: FSM based Client ID of the dataset to be pushed.
    :param lang: Language code of the dataset.
    :param days: Number of days for which data needs to be pushed,
                    ex: 0 for current day, 1 for current + previous day and so on.
    :param output_file: Output file path for dataset to be saved, Default: None
    :param call_quantity: Number of random calls to be returned or saved, Default: None
    :return: fsm_dataset: Downloaded FSM Dataset
    """
    print(f"Downloading {lang} language data for Client id: {client_id} for the last {days} days")

    if output_file and os.path.exists(output_file):
        raise FileExistsError(f"{output_file} is already present")

    fsm_dataset = download_data(client_id, lang, days)

    if fsm_dataset:

        if call_quantity:
            print(f"Filtering out {call_quantity} random calls")

            fsm_dataset = filter_data(fsm_dataset, call_quantity=call_quantity)

        if output_file:
            with open(output_file, "w") as fp:
                json.dump(fsm_dataset, fp)
            print(f"Saved Downloaded data at {output_file}")
        else:
            return fsm_dataset
    else:
        raise RuntimeError("No data found, please check your input values")


def main():
    """
    Function for CLI access, will be deprecated in the following versions
    """
    args = docopt(__doc__, version=__version__)

    if args["pull"]:

        pull(args["--client-id"], args["--lang"], args["--days"], args["--output-json"], args["--call-quantity"])

    else:
        raise NotImplementedError("Currently only fsm pull is supported")
