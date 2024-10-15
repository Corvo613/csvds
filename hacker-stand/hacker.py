from flask import Flask, render_template

app = Flask(__name__)

home_url = "http://home.com:8080"

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/csrf")
def csrf():
    return render_template('csrf.html')

@app.route("/cors")
def cors():
    return render_template('cors.html')

@app.route('/csrf/vuln', methods=['GET'])
def csrf_vuln_get():
    return render_template('csrf_vuln.html')

@app.route('/csrf/token', methods=['GET'])
def csrf_vuln_get_token():
    return render_template('csrf_token.html')

@app.route('/secret-key')
def secret_key():
    # Секретный ключ
    return 'Секретный ключ: 12345678900'

if __name__ == '__main__':
    app.run(host='hacker.com', port=8081)