"""
Command line interface for interacting with FSM data server

Usage:
fsm-pull --org-id=<org-id> --lang-code=<lang-code> --start=<DDMMYYYY> --output-json=<output-json> [--end=<DDMMYYYY>] \
[--call-quantity=<call-quantity>]
fsm-pull (-h|--help)

Options:
--org-id=<org-id>                   Client Organisation ID for the client for which data is to be downloaded
--lang-code=<lang-code>             Language code, en for english, hi for hindi etc
--start=<DDMMYYYY>                  Start Date from which data is to be downloaded,
                                                If start date is 15th August 1947, Please enter 15081947
--end=<DDMMYYYY>                    End Date till which data is to be downloaded,
                                                If start date is 15th August 1947, Please enter 15081947
                                                Default is end of current date
--call-quantity=<call-quantity>     Number of call to be downloaded, Default is 0(all the calls)
"""

import os
import json
import time

from docopt import docopt
from typing import Optional
from datetime import datetime, timedelta
from loguru import logger

from fsm_pull import __version__
from fsm_pull.connection import Connection


def convert_date(date_string: str) -> str:

    if date_string == "now":
        return (datetime.now() + timedelta(days=1)).strftime(
            "%Y-%m-%d"
        ) + "T00:00:00+05:30"

    try:

        if len(date_string) == 8:
            given_date = datetime.strptime(date_string, "%d%m%Y")
            if (
                datetime.strptime("01062016", "%d%m%Y")
                <= given_date
                <= (datetime.now() + timedelta(days=1))
            ):
                return given_date.strftime("%Y-%m-%d") + "T00:00:00+05:30"

        raise ValueError

    except ValueError:
        raise ValueError(
            "Please check date format and if date is in range,"
            "If date is 5th August 1947, Please enter 05081947(DDMMYYYY)"
        )


def parse_metadata_json(conversations):
    for conversation in conversations:
        if "metadata" in conversation:
            conversation["metadata"] = json.loads(conversation["metadata"])
    return conversations


def get_call_list(
    org_id: int,
    lang_code: str,
    start: str,
    end: str = "now",
    call_quantity: int = 0,
    flow_uuid: Optional[str] = None,
):
    start = convert_date(start)
    end = convert_date(end)

    new_connection = Connection(org_id)
    proc_start_time = time.time()
    print(
        f"Downloading {call_quantity if call_quantity else 'all'} Call(s) made between {start} and {end}"
    )

    call_list = []
    turn_count = 0
    calls = new_connection.fetch_calls(lang_code, start, end, call_quantity, flow_uuid=flow_uuid)

    for call in calls:
        turns = new_connection.fetch_turns(call["uuid"])
        turns["conversations"] = parse_metadata_json(turns["conversations"])

        if "virtual_number" in turns:
            call["virtual_number"] = turns["virtual_number"]

        call["turns"] = turns
        turn_count += len(turns)

        call_list.append(call)

    logger.info(f"pulled {len(calls)} calls ({turn_count} turns) in {time.time() - proc_start_time:.2f}s")
    return call_list


def pull(
    org_id: int,
    lang_code: str,
    start: str,
    end: str = "now",
    call_quantity: int = 0,
    output_json: Optional[str] = None,
):

    if output_json and os.path.exists(output_json):
        raise FileExistsError(f"{output_json} already present")

    call_list = get_call_list(
        org_id, lang_code, start, end=end, call_quantity=call_quantity
    )

    if output_json:
        print(f"Writing {len(call_list)} call(s) to {output_json}")
        with open(output_json, "w") as f:
            json.dump(call_list, f)
    else:
        print(f"Returning {len(call_list)} call(s)")
        return call_list


def main():
    args = docopt(__doc__, version=__version__)

    org_id = args["--org-id"]
    lang_code = args["--lang-code"]
    start = args["--start"]
    output_json = args["--output-json"]

    end = args["--end"] or "now"
    call_quantity = int(args["--call-quantity"] or 0)

    pull(org_id, lang_code, start, end, call_quantity, output_json)
