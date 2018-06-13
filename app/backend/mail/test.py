import requests


course_id = None
res = requests.get('http://localhost:5000/api/courses')
if (res.status_code == 200):
    courses = res.json()
    course_id = courses["json_data"][0]["id"]
    #print(courses["json_data"])
    # for course in courses['json_data']:
    #     print(course['id'])
else:
    print("Error retrieving course")

if (course_id == None):
    print("invalid course id")
    exit()
else:
    print(course_id)

inject_label2 = requests.post('http://localhost:5000/api/labels/' + course_id)
inject_label1 = requests.post('http://localhost:5000/api/labels/' + course_id)

if (inject_label1.status_code != 200):
    print("Error setting label 1")
    #print(inject_label1.text)
    print(inject_label1)
if (inject_label2.status_code != 200):
    print("Error setting label 2")
    print(inject_label2)

res = requests.get('http://localhost:5000/api/labels/' + course_id)
if (res.status_code == 200):
    labels = res.json()
    print(labels)
    print(labels["json_list"])
else:
    print("Error retrieving labels")
