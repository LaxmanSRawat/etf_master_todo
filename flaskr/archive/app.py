from flask import Flask, url_for, request, make_response, redirect,abort, render_template

app = Flask(__name__)

@app.route("/")
def hello_world():
    username = request.cookies.get('username')
    resp = make_response("<p>Welcome to ETF To Do backend!</p>")
    resp.set_cookie('username','Laxman')
    print(f'the user is {username}')
    return resp

@app.route('/gobacktohome/')
def go_back_to_home():
    return redirect(url_for('hello_world'))

@app.route('/<string:input>')
def print_input_integer(input):
    return f'<p>You have given {input} as an route input'

@app.route('/url_parameters/', methods = ['GET'])
def print_parameter():
    key=request.args.get('key')
    return f'<p>You have given value to parameter key = {key}'

@app.route('/login')
def login():
    abort(500)
    print("this won't be executed")

@app.errorhandler(500)
def custom_server_error(error):
    return '<p> THERE IS A SERVER ERROR <b> AAAAAAAAAAAAAAAAAAAAA! </b> </P>', 500

@app.route('/invoke_logs', methods = ['GET'])
def invoke_logs():
    app.logger.debug('This is debugging log')
    app.logger.warning('This is a warning')
    app.logger.error('This is an error')
    return '<p> Check logs on server </p>'

with app.test_request_context():
    print(url_for('hello_world'))
    print(url_for('print_input_integer', input ='Hello world'))


with app.test_request_context('/',method='GET'):
    assert request.path == '/'
    assert request.method == 'GET'