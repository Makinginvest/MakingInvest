def convert_bson_json(data: any):
    if data == None:
        return None
    data["_id"] = str(data["_id"])
    return data
