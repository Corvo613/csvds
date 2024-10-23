from flask import Flask, render_template

application = Flask(__name__)

home_url = "http://home.com:8080"

@application.route("/")
def index():
    return render_template('index.html', home_url=home_url)

@application.route("/csrf")
def csrf():
    return render_template('csrf.html', home_url=home_url)

@application.route("/cors")
def cors():
    return render_template('cors.html', home_url=home_url)

@application.route('/csrf/vuln', methods=['GET'])
def csrf_vuln_get():
    return render_template('csrf_vuln.html', home_url=home_url)

@application.route('/csrf/token', methods=['GET'])
def csrf_vuln_get_token():
    return render_template('csrf_token.html', home_url=home_url)

if __name__ == '__main__':
    application.run(host='0.0.0.0')