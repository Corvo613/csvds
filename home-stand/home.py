from flask import Flask, request, render_template, make_response, session, redirect
import uuid

application = Flask(__name__)
application.config['SECRET_KEY'] = "7f4c71fd04a55fc1a9add736d030a707c55ff375697e729190b63b7f20a95a817fca9d423423d947dda9ddcb73e88adc8fe5f5f0aad06bd7885a755290f8f68b"
application.config["SESSION_PERMANENT"] = False
application.config["SESSION_TYPE"] = "filesystem"
application.config["SESSION_COOKIE_HTTPONLY"] = False

@application.route("/")
def index():
    try:
        if request.cookies["session"]:
            authorized_color = "green"
    except:
         authorized_color = "red"
        
    secret_key = session.get('secret_key', default="Пока ничего :(")
    
    return render_template("index.html", authorized_color=authorized_color, secret_key=secret_key)

@application.route("/auth", methods=["POST"])
def auth():
    secure = request.form.get("secure", False)
    httponly = request.form.get("httponly", False)
    samesite = request.form.get("samesite", "Lax")

    if secure == "on":
        application.config["SESSION_COOKIE_SECURE"] = True
    else: 
        application.config["SESSION_COOKIE_SECURE"] = False

    if httponly == "on":
        application.config["SESSION_COOKIE_HTTPONLY"] = True
    else: 
        application.config["SESSION_COOKIE_HTTPONLY"] = False

    if samesite == "Strict":
        application.config["SESSION_COOKIE_SAMESITE"] = "Strict"
    elif samesite == "Lax":
        application.config["SESSION_COOKIE_SAMESITE"] = "Lax"
    elif samesite == "None":
        application.config["SESSION_COOKIE_SAMESITE"] = "None"
    else:
        application.config["SESSION_COOKIE_SAMESITE"] = None

    session['csrf_token'] = str(uuid.uuid4())
    session['critical_action'] = False
    session['secret_key'] = "0JIg0JDQu9GM0YTQsC3QkdCw0L3QutC1INGA0LDQsdC+0YLQsNGO0YIg0YLQvtC70YzQutC+INC60L7RgtC40LrQuCA6Mw=="

    return redirect("/")

@application.route("/xss/vuln")
def xss_vuln():
    query = request.args.get("query")
    return render_template("xss_vuln.html", query=query)

@application.route("/xss/encoding")
def xss_encoding():
    query = request.args.get("query")
    return render_template("xss_encoding.html", query=query)

@application.route("/xss/csp")
def xss_csp():
    query = request.args.get("query")
    response = make_response(render_template("xss_csp.html", query=query))
    response.headers["Content-Security-Policy"] = "script-src 'self' 'unsafe-hashes' 'sha256-/V0eTC15ql0NHNrLIk5jJ/k8ADy7TG0dMFXrBR6wT+M='"
    return response

@application.route("/csrf/vuln", methods=["GET"])
def csrf_vuln_get():
    return render_template("csrf_vuln.html")

@application.route("/csrf/vuln", methods=["POST"])
def csrf_vuln_post():
    session['critical_action'] = True
    return redirect("/csrf/vuln")

@application.route("/csrf/token", methods=["GET"])
def csrf_vuln_token():
    return render_template("csrf_token.html", csrf_token = session.get("csrf_token"))

@application.route("/csrf/token", methods=["POST"])
def csrf_token():
    token = request.form["token"]
    if token == session.get("csrf_token"):
        session["critical_action"] = True
        return redirect("/csrf/token")
    return "Invalid CSRF-token"

@application.route("/disclosure")
def disclosure():
    return render_template("disclosure.html")

@application.after_request
def after_request(response):
    response.headers["Access-Control-Allow-Origin"] = request.headers.get("Origin")
    response.headers["Access-Control-Allow-Credentials"] = "true"
    return response

if __name__ == "__main__":
    application.run(host="0.0.0.0")