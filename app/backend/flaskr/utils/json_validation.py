def validate_json(json_data, tags):
    '''
    Requires a jsondata object and an array of strings (keys)
    it should contain, returns true if complete.
    '''
    if json_data is None:
        return False

    for tag in tags:
        if tag not in json_data:
            return False

    return True


def validate_ticket_data(ticket_data):

    max_id = 1000000000
    min_id = 10000

    # Check all required fields
    required_tags = ['message', 'subject', 'courseid',
                     'studentid', 'name', 'email']

    for tag in required_tags:
        if tag not in ticket_data:
            return False

    # Check subject validity
    if len(ticket_data['subject']) > 50:
        return False

    # Check message validity
    if len(ticket_data['message']) < 1 or len(ticket_data['message']) > 10000:
        return False

    # Check if student data is provided by current_identity
    lenname = len(ticket_data['name']) < 1
    lenemail = len(ticket_data['email']) < 1

    if lenname or lenemail:
        return False

    if ticket_data['studentid'] > max_id or ticket_data['studentid'] < min_id:
        return False

    return True
