#!/usr/bin/env python3 -u
# Note: the -u denotes unbuffered (i.e output straing to stdout without buffering data and then writing to stdout)

import json
import os
import sys
from datetime import datetime

FIELDS_TO_PARSE = ['holding_stock', 'holding_quantity']


def parse_create(payload_after, op_type):
    current_ts = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    out_tuples = []
    for field_to_parse in FIELDS_TO_PARSE:
        out_tuples.append(
            (
                payload_after.get('holding_id'),
                payload_after.get('user_id'),
                field_to_parse,
                None,
                payload_after.get(field_to_parse),
                payload_after.get('datetime_created'),
                None,
                None,
                current_ts,
                op_type
            )
        )

    return out_tuples


def parse_delete(payload_before, ts_ms, op_type):
    current_ts = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    out_tuples = []
    for field_to_parse in FIELDS_TO_PARSE:
        out_tuples.append(
            (
                payload_before.get('holding_id'),
                payload_before.get('user_id'),
                field_to_parse,
                payload_before.get(field_to_parse),
                None,
                None,
                ts_ms,
                current_ts,
                op_type
            )
        )

    return out_tuples


def parse_update(payload, op_type):
    current_ts = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    out_tuples = []
    for field_to_parse in FIELDS_TO_PARSE:
        out_tuples.append(
            (
                payload.get('after', {}).get('holding_id'),
                payload.get('after', {}).get('user_id'),
                field_to_parse,
                payload.get('before', {}).get(field_to_parse),
                payload.get('after', {}).get(field_to_parse),
                None,
                payload.get('ts_ms'),
                None,
                current_ts,
                op_type
            )
        )

    return out_tuples


def parse_payload(input_raw_json):
    input_json = json.loads(input_raw_json)
    op_type = input_json.get('payload', {}).get('op')
    if op_type == 'c':
        return parse_create(
            input_json.get('payload', {}).get('after', {}),
            op_type
        )
    elif op_type == 'd':
        return parse_delete(
            input_json.get('payload', {}).get('before', {}),
            input_json.get('payload', {}).get('ts_ms', None),
            op_type
        )
    elif op_type == 'u':
        return parse_update(
            input_json.get('payload', {}),
            op_type
        )
    # no need to log read events
    return []


for line in sys.stdin:
    # 1. reads line from unix pipe, assume only valid json come through
    # 2. parse the payload into a format we can use
    # 3. prints out the formatted data as a string to stdout
    # 4. the string is of format
    #    holding_id, user_id, change_field, old_value, new_value, datetime_created, datetime_updated, datetime_deleted, datetime_inserted
    data = parse_payload(line)
    for log in data:
        log_str = ','.join([str(elt) for elt in log])
        print(log_str, flush=True)

