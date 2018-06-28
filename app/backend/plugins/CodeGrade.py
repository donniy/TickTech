'''
Demo Plugin - This plugin is not connected to an api and will return
demo data.
'''

display_name = "CodeGrade"

course_settings = {
    'api_key': {
        'type': 'string',
        'default': '',
        'display_name': 'Api key',
        'help_text': 'Can be found on the account page on DemoPlugin.io'
    },
    'feedback': {
        'type': 'string',
        'default': '',
        'display_name': 'Code Feedback',
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
    Returns the ta of this student. Should receive an assignment_id that is
    int the format of the api this plugin suppors.

    Demo: This returns the id of demo TA Erik Kooistra.
    '''
    return 11111


def get_assignment_info(course_settings, student_id, assignment_id):
    '''
    Returns info about the assignment made by this student. The response
    should be a dict.
    '''
    tmp = {}
    tmp['Grade'] = {'type': 'grade', 'value': course_settings['grade']}
    tmp['Feedback'] = {'type': 'text', 'value': course_settings['feedback']}
    tmp['Assignment'] = {'type': 'url', 'value': 'https://www.google.com'}
    tmp['Visit CodeGrade'] = {'type': 'url', 'value': 'https://codegra.de'}
    return tmp
