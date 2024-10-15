from flask import Flask, request, render_template, jsonify, make_response, session, redirect
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = "7f4c71fd04a55fc1a9add736d030a707c55ff375697e729190b63b7f20a95a817fca9d423423d947dda9ddcb73e88adc8fe5f5f0aad06bd7885a755290f8f68b"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_COOKIE_HTTPONLY"] = False

@app.route("/")
def index():
    try:
        if request.cookies["session"]:
            authorized_color = "green"
    except:
         authorized_color = "red"
        
    secret_key = session.get('secret_key', default="Пока ничего :(")
    
    return render_template("index.html", authorized_color=authorized_color, secret_key=secret_key)

@app.route("/auth", methods=["POST"])
def auth():
    secure = request.form.get("secure", False)
    httponly = request.form.get("httponly", False)
    samesite = request.form.get("samesite", "Lax")

    if secure == "on":
        app.config["SESSION_COOKIE_SECURE"] = True
    else: 
        app.config["SESSION_COOKIE_SECURE"] = False

    if httponly == "on":
        app.config["SESSION_COOKIE_HTTPONLY"] = True
    else: 
        app.config["SESSION_COOKIE_HTTPONLY"] = False

    if samesite == "Strict":
        app.config["SESSION_COOKIE_SAMESITE"] = "Strict"
    elif samesite == "Lax":
        app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
    elif samesite == "None":
        app.config["SESSION_COOKIE_SAMESITE"] = "None"
    else:
        app.config["SESSION_COOKIE_SAMESITE"] = None

    session['csrf_token'] = str(uuid.uuid4())
    session['critical_action'] = False
    session['secret_key'] = "0JIg0JDQu9GM0YTQsC3QkdCw0L3QutC1INGA0LDQsdC+0YLQsNGO0YIg0YLQvtC70YzQutC+INC60L7RgtC40LrQuCA6Mw=="

    return redirect("/")

@app.route("/xss/vuln")
def xss_vuln():
    query = request.args.get("query")
    return render_template("xss_vuln.html", query=query)

@app.route("/xss/encoding")
def xss_encoding():
    query = request.args.get("query")
    return render_template("xss_encoding.html", query=query)

@app.route("/xss/csp")
def xss_csp():
    query = request.args.get("query")
    response = make_response(render_template("xss_csp.html", query=query))
    response.headers["Content-Security-Policy"] = "script-src 'none'; object-src 'none'"
    return response

@app.route("/csrf/vuln", methods=["GET"])
def csrf_vuln_get():
    return render_template("csrf_vuln.html")

@app.route("/csrf/vuln", methods=["POST"])
def csrf_vuln_post():
    session['critical_action'] = True
    return redirect("/csrf/vuln")

@app.route("/csrf/token", methods=["GET"])
def csrf_vuln_token():
    return render_template("csrf_token.html", csrf_token = session.get("csrf_token"))

@app.route("/csrf/token", methods=["POST"])
def csrf_token():
    token = request.form["token"]
    if token == session.get("csrf_token"):
        session["critical_action"] = True
        return redirect("/csrf/token")
    return "Invalid CSRF-token"

@app.route("/disclosure")
def disclosure():
    return render_template("disclosure.html")

@app.after_request
def after_request(response):
    response.headers["Access-Control-Allow-Origin"] = request.headers.get("Origin")
    response.headers["Access-Control-Allow-Credentials"] = "true"
    return response

if __name__ == "__main__":
    app.run(host="home.com", port=8080)