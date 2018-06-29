'''
Demo Plugin - This plugin is not connected to an api and will return
demo data.
'''

display_name = "Demo Plugin"

course_settings = {
    'api_key': {
        'type': 'string',
        'default': '',
        'display_name': 'Api key',
        'help_text': 'Can be found on the account page on DemoPlugin.io'
    },
    'demo_setting': {
        'type': 'string',
        'default': '',
        'display_name': 'Demo Setting',
        'help_text': ''
    },
    'grade': {
        'type': 'number',
        'default': 5,
        'display_name': 'Grade',
        'help_text': 'This will always be returned as the grade.'
    }
}


def get_ta(course_settings, student_id, assignment_id):
    '''
    Returns the teaching assistant of this student.
    Should receive an assignment_id that is
    in the format of the api this plugin suppors.

    Demo: This returns the id of demo teaching assistant Erik Kooistra.
    '''
    return 50637080


def get_assignment_info(course_settings, student_id, assignment_id):
    '''
    Returns info about the assignment made by this student. The response
    should be a dict.
    '''
    tmp = {}
    tmp['Grade'] = {'type': 'grade', 'value': course_settings['grade']}
    tmp['Feedback'] = {'type': 'text', 'value': 'Code was not PEP8 compliant.'}
    tmp['Assignment'] = {'type': 'text', 'value': assignment_id}
    return tmp
