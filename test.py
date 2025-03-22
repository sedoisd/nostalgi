from requests import get

server = 'http://localhost:8080/api/'
response_all_jobs = get(f'{server}jobs')
response_correct_one_job = get(f'{server}jobs/1')
error_response_by_id_job = get(f'{server}jobs/99')
error_response_by_str = get(f'{server}jobs/q')

print(f'all jobs - {response_all_jobs}, {response_all_jobs.json()}')
print(f'one job - {response_correct_one_job}, {response_correct_one_job.json()}')
print(f'error request by id - {error_response_by_id_job}, {error_response_by_id_job.json()}')
print(f'error request by str - {error_response_by_str}, {error_response_by_str.json()}')