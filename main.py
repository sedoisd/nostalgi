import base64
import datetime
from io import BytesIO
from PIL import Image
from flask import Flask, render_template, redirect, request, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_restful import abort, Api

from data import db_session, users_resource  # , jobs_api

from data.departments import Department
from data.hazard import Hazard
from data.static import get_map_by_toponym
from forms.department import DepartmentForm
from data.jobs import Jobs
from forms.job import JobForm
from data.users import User
from forms.user import RegisterForm, LoginForm

app = Flask(__name__)

api = Api(app)
api.add_resource(users_resource.UsersListResource, '/api/v2/users')

api.add_resource(users_resource.UsersResource, '/api/v2/users/<int:user_id>')

login_manager = LoginManager()
login_manager.init_app(app)

app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(
    days=31
)


# @app.errorhandler(404)
# def not_found(error):
#     return make_response(jsonify({'error': 'Not found'}), 404)


# @app.errorhandler(400)
# def bad_request(_):
#     return make_response(jsonify({'error': 'Bad Request'}), 400)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


def main():
    db_session.global_init("db/2.db")
    # app.register_blueprint(jobs_api.blueprint)

    app.run(port=8080, host='127.0.0.1')

    # session = db_session.create_session()
    # job = session.query(Jobs).filter(Jobs.id == 4).first()
    # hazard = session.query(Hazard).filter(Hazard.id == 5).first()
    # job.hazard.append(hazard)
    # print(job.vivod())
    # # for user in session.query(User, Jobs).all():
    # #     print(user)
    # session.commit()


@app.route("/")
def index():
    session = db_session.create_session()
    list_work = list(session.query(Jobs))
    return render_template('index.html', list_work=list_work)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.login_or_email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.login_or_email.data,
            surname=form.surname.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/departments')
def departments():
    session = db_session.create_session()
    all_departments = list(session.query(Department))
    return render_template('list_departments.html', departments=all_departments)


@app.route('/department', methods=['GET', 'POST'])
@login_required
def add_department():
    form = DepartmentForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        department = Department()
        department.title = form.title.data
        department.chief = form.chief.data
        department.members = form.members.data
        department.email = form.email.data
        db_sess.add(department)
        db_sess.commit()
        return redirect('/departments')
    return render_template('department.html', title='Добавление департамента',
                           form=form)


@app.route('/department/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_department(id):
    form = DepartmentForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        department = db_sess.query(Department).filter(Department.id == id,
                                                      Department.chief_user == current_user).first()
        if current_user.id == 1:
            department = db_sess.query(Department).filter(Department.id == id).first()
        if department:
            form.title.data = department.title
            form.chief.data = department.chief
            form.members.data = department.members
            form.email.data = department.email
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        department = db_sess.query(Department).filter(Department.id == id,
                                                      Department.chief_user == current_user).first()
        if current_user.id == 1:
            department = db_sess.query(Department).filter(Department.id == id).first()
        if department:
            department.title = form.title.data
            department.chief = form.chief.data
            department.members = form.members.data
            department.email = form.email.data
            db_sess.commit()
            return redirect('/departments')
        else:
            abort(404)
    return render_template('department.html',
                           title='Редактирование департамента',
                           form=form
                           )


@app.route('/department_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def department_delete(id):
    db_sess = db_session.create_session()
    department = db_sess.query(Department).filter(Department.id == id,
                                                  Department.chief_user == current_user).first()
    if current_user.id == 1:
        department = db_sess.query(Department).filter(Department.id == id).first()
    if department:
        db_sess.delete(department)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/departments')


@app.route('/job', methods=['GET', 'POST'])
@login_required
def add_job():
    form = JobForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = Jobs()
        job.job = form.title.data
        job.team_leader = form.team_leader.data
        job.work_size = form.duration.data
        job.collaborators = form.collaborators.data
        job.is_finished = form.is_finished.data
        db_sess.add(job)
        db_sess.commit()
        return redirect('/')
    return render_template('job.html', title='Добавление работы',
                           form=form)


@app.route('/job/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_job(id):
    form = JobForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        job = db_sess.query(Jobs).filter(Jobs.id == id, Jobs.user == current_user).first()
        if current_user.id == 1:
            job = db_sess.query(Jobs).filter(Jobs.id == id).first()
        if job:
            form.title.data = job.job
            form.team_leader.data = job.team_leader
            form.duration.data = job.work_size
            form.collaborators.data = job.collaborators
            form.is_finished.data = job.is_finished
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = db_sess.query(Jobs).filter(Jobs.id == id, Jobs.user == current_user).first()
        if current_user.id == 1:
            job = db_sess.query(Jobs).filter(Jobs.id == id).first()
        if job:
            job.job = form.title.data
            job.team_leader = form.team_leader.data
            job.work_size = form.duration.data
            job.collaborators = form.collaborators.data
            job.is_finished = form.is_finished.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('job.html',
                           title='Редактирование работы',
                           form=form
                           )


@app.route('/job_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def job_delete(id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).filter(Jobs.id == id,
                                     Jobs.user == current_user
                                     ).first()
    if current_user.id == 1:
        job = db_sess.query(Jobs).filter(Jobs.id == id).first()
    if job:
        db_sess.delete(job)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')

@app.route('/users_show/<int:user_id>')
def user_show(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == user_id).first()
    if user:
        params = {'name': f'{user.surname} {user.name}', 'city': user.city_from}
        image = Image.open(BytesIO(get_map_by_toponym(params['city']).content))
        path = 'static/image/nostalgi.png'#.format(image.format)
        image.save(path)
        params['image'] = path
        print(params)

        return render_template('nostalgia.html', params=params)
    return 'error'
if __name__ == '__main__':
    main()
