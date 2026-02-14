import json
import os
from jsonschema import validate, ValidationError

SCHEMA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'schema')

def load_schema(name):
    path = os.path.join(SCHEMA_DIR, f"{name}.schema.json")
    with open(path, 'r') as f:
        return json.load(f)

def validate_state(data):
    schema = load_schema('state')
    try:
        validate(instance=data, schema=schema)
        return True, None
    except ValidationError as e:
        return False, e.message

def validate_session(data):
    schema = load_schema('session')
    try:
        validate(instance=data, schema=schema)
        return True, None
    except ValidationError as e:
        return False, e.message
