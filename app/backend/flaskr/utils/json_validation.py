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

def validate_ticket_data(ticket_data):

    # Check all required fields
    required_tags = ['message', 'subject', 'courseid', 'studentid', 'name', 'email']
    for tag in required_tags:
        if tag not in ticket_data:
            return False

    # Check
    if len(ticket_data['message']) > 50 or < 1:
        return False
