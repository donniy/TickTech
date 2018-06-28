'''
Demo Plugin - This plugin is not connected to an api and will return
demo data.
'''

display_name = "Demo Plugin"


def get_ta(student_id, assignment_id):
    '''
    Returns the teaching assistant of this student.
    Should receive an assignment_id that is
    in the format of the api this plugin suppors.

    Demo: This returns the id of demo TA Erik Kooistra.
    '''
    return 11111


def get_assignment_info(student_id, assignment_id):
    '''
    Returns info about the assignment made by this student. The response
    should be a dict.
    '''
    tmp = {}
    tmp['Grade'] = {'type': 'grade', 'value': 5}
    tmp['Feedback'] = {'type': 'text', 'value': 'Code was not PEP8 compliant.'}
    tmp['Assignment'] = {'type': 'url', 'value': 'https://www.google.com'}
    return tmp
