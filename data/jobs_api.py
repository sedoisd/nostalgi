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