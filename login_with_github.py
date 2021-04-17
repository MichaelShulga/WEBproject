from flask import Flask
from flask import url_for, redirect
from flask_dance.contrib.github import make_github_blueprint, github


app = Flask(__name__)
app.config["SECRET_KEY"] = "SECRET KEY dwqdqdwqdqwdqdwqw "


github_blueprint = make_github_blueprint(client_id='286f1e39d77a4617afa8',
                                         client_secret='c74e7fe34c34a9dd75d0ac949ba9bcfee420933c')

app.register_blueprint(github_blueprint, url_prefix='/github_login')


@app.route('/')
def github_login():
    if not github.authorized:
        return redirect(url_for('github.login'))
    else:
        account_info = github.get('/user')
        if account_info.ok:
            account_info_json = account_info.json()
            return '<h1>Your Github name is {}'.format(account_info_json['login'])

    return '<h1>Request failed!</h1>'


if __name__ == "__main__":
    app.run(port=8083, host='127.0.0.1', debug=True, ssl_context=('cert.pem', 'key.pem'))
