import flask
from flask import make_response, jsonify

from . import db_session
from .jobs import Jobs

blueprint = flask.Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs')
def get_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs)
    if not jobs:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify({'jobs': [job.to_dict(
        only=('id', 'team_leader', 'job', 'work_size', 'collaborators', 'start_date', 'end_date', 'is_finished')) for
        job in jobs]})


@blueprint.route('/api/jobs/<int:job_id>', methods=['GET'])
def get_one_news(job_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(job_id)
    if not job:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify({'job': job.to_dict(
        only=('id', 'team_leader', 'job', 'work_size', 'collaborators', 'start_date', 'end_date', 'is_finished'))})
