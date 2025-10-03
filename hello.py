from flask import Flask

app = Flask(__name__)

# @app.route("/")
# def hello_world():
#     return "<h1>Hello world</h1>"

@app.route('/')
def index():
    return 'Index Page'

@app.route('/hello/')
def hello():
    return 'Hello, World'

@app.route('/login')
def login():
    data = {"username":"thanawat","grade":"A"}
    return data

@app.route('/users/<username>')
def w_user(username):
    return f'{username}\'s sites'

# from flask import url_for

# with app.test_request_context():
    # print(url_for('index'))
    # print(url_for('hello'))
    # print(url_for('login'))
    # print(url_for('login', next='/'))
    # print(url_for('w_user', username='John Doe'))