from pprint import pprint

from requests import get, post, delete

server = 'http://localhost:8080/api/v2/'
request_for_list_user_resource = f'{server}users'
get_request_user_resource = lambda user_id: f'{server}users/{user_id}'

# DATA
json_add_user_1 = {'address': 'Boston',
                   'age': 21,
                   'email': 'Bostone_Capone@mars.org',
                   'name': '',
                   'position': '123',
                   'speciality': '312',
                   'surname': '12'}
json_add_user_2 = {'address': 'Destr',
                   'age': 24,
                   'email': 'Caro_De_Mireko@mars.org',
                   'name': 'Caro',
                   'position': 'fdf',
                   'speciality': 'fsad',
                   'surname': 'fds'}


def request_get_all_user():
    response_on_get_all_user = get(request_for_list_user_resource)
    pprint(response_on_get_all_user.json())


def add_user(json=None):
    response_add_user = post(request_for_list_user_resource, json=json)
    print([response_add_user.json()])
    return response_add_user.json()


def get_user(user_id):
    response_get_user = get(get_request_user_resource(user_id))
    print(response_get_user.json())


def delete_user(user_id):
    response_delete_user = delete(get_request_user_resource(user_id))
    print(response_delete_user.json())


# GET REQUEST ON ALL USER LIST
request_get_all_user()

# POST REQUEST ON ADD USERS
id_1 = add_user(json_add_user_1)['id']
id_2 = add_user(json_add_user_2)['id']
# print(id_1, id_2)
# response = post(request_for_list_user_resource, json=json)

# GET REQUEST ON CERTAIN USER
get_user(id_1)
get_user(id_2)

# DELETE REQUEST ON CERTAIN USER
delete_user(id_1)
delete_user(id_2)
request_get_all_user()
