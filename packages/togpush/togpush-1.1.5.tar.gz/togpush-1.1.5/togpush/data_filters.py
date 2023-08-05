"""
Functions for filtering dataset.

Turn level only accepts dataset with only audio user input, doesn't matter for call level
"""

import random

fsm_dataset_format = {"alternatives": list, "audio_url": str, "call_id": int,
                      "reftime": str, "debug_metadata": dict, "metadata": dict,
                      "prediction": dict, "state": str, "sub_type": str,
                      "text": str, "conversation_id": int, "type": str
                      }


def check_data_format(dataset: list):
    """
    Check if the dataset provided is in the right format as per the scheme provided the documentation,
    only a single random data points is checked from the whole dataset.
    """

    format_flag = 1

    check_index = random.choice(range(0, len(dataset)-1))

    for key, value in fsm_dataset_format.items():
        try:
            if isinstance(dataset[check_index][key], value):
                continue
            else:
                format_flag = 0
                print(f"{key} must be of type: {fsm_dataset_format[key]}")
        except KeyError:
            raise KeyError("Incorrect format, please check togpush/data_format.json")
    if format_flag:
        return True
    else:
        return False


def extract_only_user(dataset: list):
    """
    Return dataset with only user input by speech
    """
    new_dataset = []

    for entry in dataset:
        if entry["type"] == "INPUT" and entry["sub_type"] == "AUDIO":
            new_dataset.append(entry)

    print(f"Returning {len(new_dataset)} turns belonging to User input(type: INPUT and sub_type: AUDIO)")

    return new_dataset


def remove_unknown(dataset: list):
    """
    The definition of unknown in this case is, entries not having ASR alternatives
    """
    new_dataset = []

    for entry in dataset:
        if not (entry["type"] == "INPUT" and entry["sub_type"] == "AUDIO"):
            raise ValueError(f"Remove unknown filter only supports Audio User Input, "
                             f"found data of type: {entry['type']} and subtype: {entry['sub_type']}")

        if "alternatives" in entry and entry["alternatives"] and entry["alternatives"][0]:
            new_dataset.append(entry)
    return new_dataset


def filter_intent(dataset, intent_name, filter_level="turn"):
    """
    Retain only the data points predicted as intent_name
    Please note "_unknown_" and "_fallback_" entries will be skipped
    """
    new_dataset = []

    if filter_level == "turn":
        for entry in dataset:
            if not (entry["type"] == "INPUT" and entry["sub_type"] == "AUDIO"):
                raise ValueError(f"Extract Intent filter only supports Audio User Input, "
                                 f"found data of type: {entry['type']} and subtype: {entry['sub_type']}")

            if entry["prediction"] and "intents" in entry["prediction"] and \
                    intent_name == entry["prediction"]["intents"][0]["name"]:
                new_dataset.append(entry)
    else:
        raise NotImplementedError("Invalid filter level, currently only turn level is supported")

    print(f"Returning {len(new_dataset)} turns with predicted intent as {intent_name}")

    return new_dataset


def filter_state(dataset, state_name, filter_level="turn"):
    """
    Retain only the data points belonging to state_name
    """
    new_dataset = []

    if filter_level == "turn":
        for entry in dataset:
            if not (entry["type"] == "INPUT" and entry["sub_type"] == "AUDIO"):
                raise ValueError(f"Extract State filter only supports Audio User Input, "
                                 f"found data of type: {entry['type']} and subtype: {entry['sub_type']}")

            if state_name in entry["state"]:
                new_dataset.append(entry)
    else:
        raise NotImplementedError("Invalid filter level, currently only turn level is supported")

    print(f"Returning {len(new_dataset)} turns belonging to {state_name} state")

    return new_dataset


def filter_unknown(dataset, filter_level="turn"):
    """
    Retain only the data points where we have no ASR alternatives
    """
    new_dataset = []

    if filter_level == "turn":
        for entry in dataset:
            if not (entry["type"] == "INPUT" and entry["sub_type"] == "AUDIO"):
                raise ValueError(f"Extract Unknown filter only supports Audio User Input, "
                                 f"found data of type: {entry['type']} and subtype: {entry['sub_type']}")

            if not entry["alternatives"][0]:
                new_dataset.append(entry)
    else:
        raise NotImplementedError("Invalid filter level, currently only turn level is supported")

    return new_dataset


def filter_quantity(dataset, filter_level: str, quantity: int):
    """
    Returns x(user input) number of randomised turns or calls.
    """
    if quantity > 0:

        if quantity >= len(dataset):
            print(f"Quantity entered({quantity}) is greater than or equal to the length of the dataset({len(dataset)}),"
                  f" returning dataset as is")
            return dataset

        random.shuffle(dataset)

        new_dataset = []

        if filter_level == "turn":

            for entry in dataset:
                if len(new_dataset) == quantity:
                    # Stop continuing once we reach the required quantity
                    break

                if entry["type"] == "INPUT" and entry["sub_type"] == "AUDIO":
                    new_dataset.append(entry)
                else:
                    raise ValueError(f"Turn level quantity filter only supports Audio User Input, "
                                     f"found data of type: {entry['type']} and subtype: {entry['sub_type']}")

            print(f"Returning {len(new_dataset)} random turns from the dataset")

        elif filter_level == "call":

            call_list = []

            for entry in dataset:
                if entry["call_id"] in call_list:
                    new_dataset.append(entry)
                else:
                    if len(call_list) < quantity:
                        call_list.append(entry["call_id"])
                        new_dataset.append(entry)

            print(f"Returning {len(call_list)} random calls from the dataset")

        else:
            raise NotImplementedError("Invalid filter level, currently only call and turn level is supported")

        return new_dataset

    else:
        raise ValueError("Quantity must be greater than or equal to 1")


def filter_data(dataset, **filter_type):
    """
    Gateway function to access data filter, Filtering happens sequentially in order of user input
    """
    for key, value in filter_type.items():

        if key == "call_quantity":
            dataset = filter_quantity(dataset, filter_level="call", quantity=int(value))
        elif key == "turn_quantity":
            dataset = filter_quantity(dataset, filter_level="turn", quantity=int(value))
        elif key == "filter_state":
            dataset = filter_state(dataset, state_name=value)
        elif key == "filter_intent":
            dataset = filter_intent(dataset, intent_name=value)
        else:
            raise NotImplementedError(f"{key} filter not supported yet, please check documentation")

    return dataset
