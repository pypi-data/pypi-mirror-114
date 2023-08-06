import csv
import uuid

from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Union

from jsonpath_ng import parse

from kicksaw_data_mapping_base import get_sheet_data
from kicksaw_data_mapping_base.constants.columns import (
    JSON_PATH,
    SFDC_OBJECT,
    SFDC_FIELD,
)
from kicksaw_data_mapping_base.constants.tokens import TOO_COMPLEX

from kicksaw_data_mapping_serializer.classes import ParseRequest, CallableDict


class KicksawSerializer:
    def __init__(
        self,
        payload: Union[List[dict]],
        default_value: Any = None,
        path_to_csv: Path = False,
    ) -> None:
        self.payload = payload
        self._default_value = default_value

        if path_to_csv:
            self._mapping_sheet = self._read_csv(path_to_csv)
        else:
            self._mapping_sheet = self._get_mapping_sheet()

        # stores fields that need the user to step in with their own python
        self._parse_requests: Dict[str, ParseRequest] = dict()
        self._processed_parse_requests: Dict[str, Any] = dict()
        self._serialized_data = self._serialize_payload()

    def get_serialized_objects(self, object_name):
        assert object_name in self._serialized_data, f"{object_name} wasn't parsed!"
        return self._serialized_data[object_name]

    def get_serialized_object(self, object_name):
        serialized_objects = self.get_serialized_objects(object_name)
        assert len(serialized_objects) == 1, f"{object_name}"
        return serialized_objects[0]

    def get_parse_requests(self):
        for parse_request in self._parse_requests.values():
            yield parse_request

    def process_parse_request(self, parse_request: ParseRequest, processed_value: Any):
        self._processed_parse_requests[parse_request.id] = processed_value

    @staticmethod
    def _get_mapping_sheet():
        return get_sheet_data()

    @staticmethod
    def _read_csv(path_to_csv):
        with open(path_to_csv) as file:
            csv_reader = csv.DictReader(file, delimiter=",")
            mappings = [row for row in csv_reader]
        return mappings

    @staticmethod
    def _index_in_list(list_: list, index: int):
        return index < len(list_)

    def _serialize_payload(self):
        object_name_to_parsed = defaultdict(list)

        for row in self._mapping_sheet:
            object_name = row[SFDC_OBJECT]
            field_name = row[SFDC_FIELD]
            json_path_expression = row[JSON_PATH]

            is_too_complex = False
            parts = json_path_expression.split(":::")
            json_path_expression = parts[0]
            if len(parts) > 1:
                special_message = parts[1]
                is_too_complex = special_message == TOO_COMPLEX

            objects = object_name_to_parsed[object_name]

            jsonpath_expr = parse(json_path_expression)
            matches = jsonpath_expr.find_or_create(self.payload)

            for idx, match in enumerate(matches):
                if not self._index_in_list(objects, idx):
                    # we use CallableDict so we can address the parse requests later on
                    objects.append(CallableDict({}))

                # find_or_create defaults to an empty dict, but we'd rather control it
                value = match.value if not match.value == {} else self._default_value

                if is_too_complex:
                    parse_request_id = str(uuid.uuid4())
                    self._parse_requests[parse_request_id] = ParseRequest(
                        parse_request_id, value, object_name, field_name
                    )
                    objects[idx][
                        field_name
                    ] = lambda parse_request_id=parse_request_id: self._processed_parse_requests.get(
                        parse_request_id, ParseRequest.UNPROCESSED
                    )
                else:
                    objects[idx][field_name] = value

        # change back to dict so if user looks up a bad object name
        # they get an exception instead of an empty list
        plain = dict(object_name_to_parsed)
        return plain
