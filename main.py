from flask import Flask, render_template, redirect, request, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_restful import Api

from forms.user import RegisterForm, LoginForm
from data.users import User
from data import db_session
from app_api import users_resources

app = Flask(__name__)
api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'secret_key'


# необходимая функция для работы всего модуля
# id -> объект User
@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


# Регистрация - ничего не изменилось
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    print(print(form.validate_on_submit()))
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Registration', form=form,
                                   message="Password mismatch")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Registration', form=form,
                                   message="This user already exists")
        user = User(email=form.email.data)
        print(user)
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Registration', form=form)


# Вход
# Предварительно нужно создать класс LoginForm и шаблон login.html
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', message="Incorrect login or password", form=form)
    return render_template('login.html', title='Authorization', form=form)


# Выход из учетной записи
# 1. декоратор login_required можно добавлять ко всем функциям, где требуется быть авторизованным
# 2. функция не возвращает страницу, а совершает действие
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/')
def index():
    return render_template('index.html')


def main():
    # database initialization
    db_session.global_init("db/blogs.db")

    # User class API
    api.add_resource(users_resources.UserListResource, '/api/v2/users')
    api.add_resource(users_resources.UserResource, '/api/v2/users/<int:user_id>')

    app.run(port=8090, host='127.0.0.1', debug=True)


if __name__ == '__main__':
    main()