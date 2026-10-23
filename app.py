"""CCC181 Week 2: a "Hello, Flask" starter app.

Run it with:
    flask --app app run --debug
then open http://127.0.0.1:5000
"""
from flask import Flask, abort, flash, redirect, render_template, request, url_for
app = Flask(__name__)
app.secret_key = "dev-only-change-me" 


SERVICES = [
    {"id": 1, "name": "New passport application"},
    {"id": 2, "name": "Passport renewal"},
    {"id": 3, "name": "Passport claiming"},
]


TICKETS = [
    {"number": 1, "name": "Raven Lamis", "email": "raven.lamis@example.com",
     "service_id": 1, "status": "waiting",
     "appointment_date": "2026-10-26", "appointment_time": "09:00"},
    {"number": 2, "name": "Kijo Dela Vega", "email": "kijo.delavega@example.com",
     "service_id": 2, "status": "waiting",
     "appointment_date": "2026-10-26", "appointment_time": "09:30"},
    {"number": 3, "name": "Winchester Cosning", "email": "winchester.cosning@example.com",
     "service_id": 3, "status": "waiting",
     "appointment_date": "2026-10-26", "appointment_time": "10:00"},
]


@app.route("/")
def index():
    # render_template looks inside the templates/ folder and passes
    # keyword arguments to the template as variables.
    return render_template("index.html", name="Ana", tickets=TICKETS)


@app.route("/queue/<int:ticket_id>")
def ticket(ticket_id):
    # <int:ticket_id> only matches numbers, so /queue/abc returns 404.
    for position, t in enumerate(TICKETS, start=1):
        if t["number"] == ticket_id:
            return render_template("ticket.html", ticket=t, position=position)
    abort(404)  # no ticket with that number


@app.route("/join")
def join_form():
    return render_template("join.html")


@app.route("/staff")
def staff_dashboard():
    return "Staff dashboard coming soon"


@app.route("/hello")
def hello():
    # The plain-string version from the Routes slide.
    return "Hello, CCC181!"


if __name__ == "__main__":
    # Lets you also start the app with: python app.py
    app.run(debug=True)
