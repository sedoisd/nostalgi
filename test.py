import pprint

from requests import get, post, delete

# def add_job(json=None):
#     response_add_job = post(f'{server}jobs', json=json)
#     try:
#         return response_add_job, response_add_job.json()
#     except Exception:
#         return response_add_job

server = 'http://localhost:8080/api/'
response_all_jobs = get(f'{server}jobs')

print(delete(f'{server}jobs/4').json())
print(delete(f'{server}jobs/4').json())
print(delete(f'{server}jobs/5').json())
print(delete(f'{server}jobs/6').json())

print(f'all jobs - {response_all_jobs}')
pprint.pprint(response_all_jobs.json())
