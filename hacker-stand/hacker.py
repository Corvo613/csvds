from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/csrf")
def csrf():
    return render_template('csrf.html')

@app.route("/cors")
def cors():
    return render_template('cors.html')

@app.route('/csrf/vuln', methods=['POST'])
def csrf_vuln():
    # Уязвимость CSRF
    return 'Вредоносный запрос принят!'

@app.route('/csrf/token', methods=['POST'])
def csrf_token():
    # Уязвимость CSRF с токеном
    return 'Вредоносный запрос принят с токеном!'

@app.route('/secret-key')
def secret_key():
    # Секретный ключ
    return 'Секретный ключ: 12345678900'

if __name__ == '__main__':
    app.run(host='hacker.com', port=8081)