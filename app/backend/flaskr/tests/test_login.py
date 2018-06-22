from flaskr.tests.utils import create_user, login


def test_retrieve_user(app, client):
    """
    Test the api call to retrieve user
    """
    create_user(app, 1234)
    auth = login(client, 1234)

    rv = client.get('/api/user/retrieve',
                    headers={
                        'Authorization': auth
                    })
    json_data = rv.get_json()['json_data']
    user = json_data['user']
    print(json_data)
    print(user['id'])
    assert rv.status == '200 OK'
    assert len(json_data) > 0
    assert user['id'] == 1234
