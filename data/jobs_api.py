import flask
from flask import make_response, jsonify, request

from . import db_session
from .jobs import Jobs

blueprint = flask.Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs', methods=['GET'])
def get_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs)
    if not jobs:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify({'jobs': [job.to_dict(
        only=('id', 'team_leader', 'job', 'work_size', 'collaborators', 'start_date', 'end_date', 'is_finished')) for
        job in jobs]})


@blueprint.route('/api/jobs/<int:job_id>', methods=['GET'])
def get_one_job(job_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(job_id)
    if not job:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify({'job': job.to_dict(
        only=('id', 'team_leader', 'job', 'work_size', 'collaborators', 'start_date', 'end_date', 'is_finished'))})


@blueprint.route('/api/jobs', methods=['POST'])
def create_job():
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    try:
        team_leader = request.json['team_leader']
        job = request.json['job']
        work_size = request.json['work_size']
        collaborators = request.json['collaborators']
        is_finished = request.json['is_finished']
        # print(request.json)
        if not (isinstance(team_leader, int) and isinstance(work_size, int) and isinstance(is_finished, bool)):
            raise Exception
    except Exception:
        return make_response(jsonify({'error': 'Bad request'}), 400)
    db_sess = db_session.create_session()
    news = Jobs(
        team_leader=team_leader,
        job=job,
        work_size=work_size,
        collaborators=collaborators,
        is_finished=is_finished
    )
    db_sess.add(news)
    db_sess.commit()
    return jsonify({'id': news.id})


@blueprint.route('/api/jobs/<int:job_id>', methods=['DELETE'])
def delete_news(job_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(job_id)
    if not job:
        return make_response(jsonify({'error': 'Not found'}), 404)
    db_sess.delete(job)
    db_sess.commit()
    return jsonify({'success': 'OK'})

@blueprint.route('/api/edit_jobs/<int:job_id>', methods=['POST'])
def edit_job(job_id):
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).filter(Jobs.id == job_id).first()
    if not job:
        return make_response(jsonify({'error': 'Not found job'}), 404)

    keys_and_type = [('team_leader', int), ('job', str), ('work_size', int), ('collaborators', str),
                     ('is_finished', bool)]
    modified_keys_and_values = dict()
    for key, correct_type in keys_and_type:
        value = request.json.get(key, None)
        if value is not None:
            if not isinstance(value, correct_type):
                return make_response(jsonify({'error': 'Bad request'}), 400)
            modified_keys_and_values[key] = value
    if len(modified_keys_and_values) != len(request.json):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    # print(modified_keys_and_values, request.json.keys())
    if 'team_leader' in modified_keys_and_values:
        job.team_leader = modified_keys_and_values['team_leader']
    elif 'job' in modified_keys_and_values:
        job.job = modified_keys_and_values['job']
    elif 'work_size' in modified_keys_and_values:
        job.work_size = modified_keys_and_values['work_size']
    elif 'collaborators' in modified_keys_and_values:
        job.collaborators = modified_keys_and_values['collaborators']
    elif 'is_finished' in modified_keys_and_values:
        job.is_finished = modified_keys_and_values['is_finished']
    db_sess.commit()
    return jsonify({'success': 'OK'})