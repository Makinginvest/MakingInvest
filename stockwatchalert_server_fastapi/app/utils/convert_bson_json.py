import json
from bson import json_util


# def convert_bson_json(d):
#     """Recursively process a dictionary, replacing $oid and $date."""
#     d = json.loads(json_util.dumps(d))  # converts BSON types to a form that the json module can handle

#     result = {}
#     for key, value in d.items():
#         if isinstance(value, dict):
#             if "$oid" in value:
#                 result[key] = value["$oid"]
#             elif "$date" in value:
#                 result[key] = value["$date"]
#             else:
#                 result[key] = convert_bson_json(value)
#         elif isinstance(value, list):
#             result[key] = [(convert_bson_json(v) if isinstance(v, dict) else v) for v in value]
#         else:
#             result[key] = value
#     return result


def convert_bson_json(d):
    """Recursively process an input, replacing $oid and $date."""
    d = json.loads(json_util.dumps(d))  # converts BSON types to a form that the json module can handle

    # Check if the input is a dictionary and process accordingly
    if isinstance(d, dict):
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
                result[key] = [convert_bson_json(v) for v in value]
            else:
                result[key] = value
        return result
    # If the input is a list, apply the conversion to each element
    elif isinstance(d, list):
        return [convert_bson_json(v) for v in d]
    else:
        # If it's neither a dict nor a list, just return the input
        return d
