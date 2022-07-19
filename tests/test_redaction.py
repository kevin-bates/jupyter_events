import pathlib

import pytest

from jupyter_events.schema import EventSchema

SCHEMA_PATH = pathlib.Path(__file__).parent / "schemas"


@pytest.mark.parametrize(
    "schema_file,redacted_policies,data,data_out",
    [
        [
            # Redact fields from objects in a nested array.
            "array.yaml",
            ["user-identifier", "user-identifiable-information"],
            {
                "nothing-exciting": "hello, world",
                "users": [
                    {"id": "test id 0", "email": "test0@testemail.com"},
                    {"id": "test id 1", "email": "test1@testemail.com"},
                ],
            },
            {
                "nothing-exciting": "hello, world",
                "users": [{}, {}],
            },
        ],
        [
            "nested-array.yaml",
            ["user-identifier", "user-identifiable-information"],
            {
                "nothing-exciting": "hello, world",
                "users": [
                    {
                        "name": "Alice",
                        "hobbies": [
                            {"sport": "basketball", "position": "guard"},
                            {"sport": "soccer", "position": "striker"},
                        ],
                    },
                    {
                        "name": "Bob",
                        "hobbies": [
                            {"sport": "basketball", "position": "center"},
                            {"sport": "soccer", "position": "goalie"},
                        ],
                    },
                ],
            },
            {
                "nothing-exciting": "hello, world",
                "users": [
                    {"hobbies": [{"sport": "basketball"}, {"sport": "soccer"}]},
                    {"hobbies": [{"sport": "basketball"}, {"sport": "soccer"}]},
                ],
            },
        ],
    ],
)
def test_redaction_in_arrays(schema_file, redacted_policies, data, data_out):
    schema = EventSchema.from_file(
        SCHEMA_PATH / "good" / schema_file, redacted_policies=redacted_policies
    )
    schema.enforce_redaction_policies(data)
    assert data == data_out
