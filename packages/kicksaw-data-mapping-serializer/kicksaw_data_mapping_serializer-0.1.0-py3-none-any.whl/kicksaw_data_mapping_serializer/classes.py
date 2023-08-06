from typing import List, Union

from kicksaw_data_mapping_base.constants.tokens import TOO_COMPLEX


class ParseRequest:
    """
    An object that contains data too complex for JsonPath
    """

    UNPROCESSED = "UNPROCESSED"

    def __init__(
        self,
        parse_request_id,
        payload_subection: Union[List[dict]],
        object_name: str,
        field_name: str,
    ) -> None:
        self.id = parse_request_id
        self.payload_subsection = payload_subection

        self.object_name = object_name
        self.field_name = field_name

    def __str__(self) -> str:
        return f"{TOO_COMPLEX} - {self.id}"

    def __repr__(self) -> str:
        return self.__str__()


class CallableDict(dict):
    """
    Keys that store a parse request object hold lambdas
    Ensures that, no matter what, that lambda is called
    whenever the dictionary is accessed, be it by:

        * printing
        * iterating
        * accessing by key
    """

    def __getitem__(self, key):
        val = super().__getitem__(key)
        if callable(val):
            return val()
        return val

    def __repr__(self):
        return repr(dict(self.items()))

    def items(self):
        evaluated = {key: self[key] for key in super().keys()}
        return evaluated.items()

    def values(self):
        return [self[key] for key in super().keys()]
