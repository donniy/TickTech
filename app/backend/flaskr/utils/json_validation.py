def validate_json(json_data, tags):
    ''' Requires a jsondata object and an array of strings (keys)
        it should contain, returns true if complete.
    '''

    if json_data is None:
        return False

    for tag in tags:
        if tag not in json_data:
            return False

    return True
