import pprint

from requests import get, post, delete

# def add_job(json=None):
#     response_add_job = post(f'{server}jobs', json=json)
#     try:
#         return response_add_job, response_add_job.json()
#     except Exception:
#         return response_add_job

def edit_job(id=None, json=None):
    response_edit_job = post(f'{server}edit_jobs/{id}', json=json)
    try:
        return response_edit_job, response_edit_job.json()
    except Exception:
        return response_edit_job

edit_json_1 = {'team_leader': 2} # Корректный запрос
edit_json_2 = {'job': 'setup uav'} # Корректный запрос
edit_json_3 = {'kartoshka': 'belen'} # Bad request - неизвестный ключ
edit_json_4 = {'work_size': 'second'} # Bad request - ошибка типа данных


server = 'http://localhost:8080/api/'
response_all_jobs = get(f'{server}jobs')

print(edit_job(6, edit_json_1))
print(edit_job(5, edit_json_2))
print(edit_job(4, edit_json_3))
print(edit_job(6, edit_json_4))


# print(f'all jobs - {response_all_jobs}')
# pprint.pprint(response_all_jobs.json())