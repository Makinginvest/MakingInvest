import json
from bson import json_util


def convert_bson_json(d):
    """Recursively process a dictionary, replacing $oid and $date."""
    d = json.loads(json_util.dumps(d))  # converts BSON types to a form that the json module can handle

    result = {}
    for key, value in d.items():
        if isinstance(value, dict):
            if "$oid" in value:
                result[key] = value["$oid"]
            elif "$date" in value:
                result[key] = value["$date"]
            else:
                result[key] = convert_bson_json(value)
        elif isinstance(value, list):
            result[key] = [convert_bson_json(v) if isinstance(v, dict) else v for v in value]
        else:
            result[key] = value
    return result
