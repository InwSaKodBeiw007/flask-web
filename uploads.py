from flask import Flask,render_template

app = Flask(__name__) 

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/<name>/images')
def user(name):
    return 'Hello {} my master'.format(name)

@app.route('/uploads')
def upanddown():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(port=8000, debug=True)