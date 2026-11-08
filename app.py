"""CCC181 Week 2: a "Hello, Flask" starter app.

Run it with:
    flask --app app run --debug
then open http://127.0.0.1:5000
"""

import os
from datetime import date, time, timedelta, timezone

from dotenv import load_dotenv
from flask import Flask, abort, flash, redirect, render_template, request, url_for
from flask_migrate import Migrate
from sqlalchemy import and_, func, or_
from sqlalchemy.exc import IntegrityError

from models import AppointmentSlot, Service, Ticket, User, db

load_dotenv()

app = Flask(__name__)
app.secret_key = "dev-only-change-me"  # Week 11 moves this into an environment variable
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
app.config["SQLALCHEMY_ECHO"] = os.environ.get("SQLALCHEMY_ECHO") == "1"

db.init_app(app)
migrate = Migrate(app, db)

PH_TIME = timezone(timedelta(hours=8))  # Philippine time has no daylight saving


@app.template_filter("local")
def local_time(value):
    """Show a database time in Philippine time, e.g. Oct 26, 08:01 AM."""
    return value.astimezone(PH_TIME).strftime("%b %d, %I:%M %p") if value else ""




APPOINTMENT_SLOTS = [
    {"value": "09:00", "label": "09:00 AM to 11:00 AM"},
    {"value": "11:00", "label": "11:00 AM to 01:00 PM"},
    {"value": "13:00", "label": "01:00 PM to 03:00 PM"},
    {"value": "15:00", "label": "03:00 PM to 05:00 PM"},
]





@app.route("/")
def index():
    # render_template looks inside the templates/ folder and passes
    # keyword arguments to the template as variables.
    return render_template("index.html", name="Ana")


@app.route('/queue/<int:ticket_id>')
@app.route('/ticket/<int:ticket_id>')
def ticket(ticket_id):
    t = db.get_or_404(Ticket, ticket_id)
    return render_template("ticket.html", ticket=t, service=t.service,
                           ahead=people_ahead(t))


@app.post("/queue/<int:ticket_id>/leave")
def leave(ticket_id):
    t = db.get_or_404(Ticket, ticket_id)
    if t.status == "waiting":
        t.status = "left"  # soft delete: the row stays for reports
        db.session.commit()
    flash("You left the queue.", "info")
    return redirect(url_for("index"))


def all_services():
    return db.session.scalars(db.select(Service).order_by(Service.name)).all()

def active_services():
    stmt = db.select(Service).filter_by(active=True).order_by(Service.name)
    return db.session.scalars(stmt).all()

def all_slots():
    return db.session.scalars(
        db.select(AppointmentSlot).order_by(AppointmentSlot.start_time)).all()


def slot_choices():
    """The slots as the join form expects them: a value and a label."""
    return [{"value": s.start_time.strftime("%H:%M"),
             "label": f"{s.start_time.strftime('%I:%M %p')} to {s.end_time.strftime('%I:%M %p')}"}
            for s in all_slots()]

def people_ahead(t):
    """Count waiting tickets for the same service that are served before t:
    an earlier appointment slot, or the same slot and an earlier created_at."""
    my_slot = t.appointment_slot
    stmt = (db.select(func.count())
            .select_from(Ticket)
            .join(AppointmentSlot)
            .where(Ticket.service_id == t.service_id,
                   Ticket.status == "waiting",
                   or_(AppointmentSlot.start_time < my_slot.start_time,
                       and_(Ticket.appointment_slot_id == t.appointment_slot_id,
                            Ticket.created_at < t.created_at))))
    return db.session.scalar(stmt)


@app.get("/join")
def join_form():
    return render_template("join.html", services=active_services(),
                           slots=slot_choices(), form={},
                           today=date.today().strftime("%B %d, %Y"))


@app.post("/join")
def join():
    form = request.form
    name = form.get("name", "").strip()
    email = form.get("email", "").strip().lower()
    service_id = form.get("service_id", type=int)
    service = db.session.get(Service, service_id) if service_id else None
    appointment_time = form.get("appointment_time", "").strip()
    slot = next((s for s in all_slots()
                 if s.start_time.strftime("%H:%M") == appointment_time), None)

    errors = {}
    if not name or len(name) > 80:
        errors["name"] = "Enter your name (up to 80 characters)."
    if "@" not in email or len(email) > 120:
        errors["email"] = "Enter a valid email address."
    if service is None or not service.active:
        errors["service_id"] = "Choose a service."
    if slot is None:
        errors["appointment_time"] = "Choose an appointment time."

    if errors:
        flash("Please fix the highlighted fields.", "danger")
        return render_template("join.html", services=all_services(),
                               slots=slot_choices(), form=form, errors=errors,
                               today=date.today().strftime("%B %d, %Y")), 400

    user = db.session.scalar(db.select(User).filter_by(email=email))
    if user is None:
        user = User(name=name, email=email)
    ticket = Ticket(user=user, service=service, appointment_slot=slot)
    db.session.add(ticket)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        flash("Something went wrong saving your ticket. Please try again.", "danger")
        return render_template("join.html", services=all_services(),
                               slots=slot_choices(), form=form, errors={},
                               today=date.today().strftime("%B %d, %Y")), 409

    flash(f"You joined the queue. Your ticket is #{ticket.id}.", "success")
    return redirect(url_for("ticket", ticket_id=ticket.id))

@app.get("/staff")
def staff_dashboard():
    service_id = request.args.get("service_id", type=int)
    slot_value = request.args.get("slot", "")
    stmt = (db.select(Ticket)
            .join(AppointmentSlot)
            .where(Ticket.status.in_(["waiting", "called"]))
            .order_by(AppointmentSlot.start_time, Ticket.created_at))
    if service_id:
        stmt = stmt.where(Ticket.service_id == service_id)
    if slot_value:
        try:
            stmt = stmt.where(AppointmentSlot.start_time == time.fromisoformat(slot_value))
        except ValueError:
            pass  # ignore a slot value that is not a time
    queue = db.session.scalars(stmt).all()
    return render_template("staff.html", tickets=queue, services=all_services(),
                           selected_service=service_id, slots=slot_choices(),
                           selected_slot=slot_value)


@app.post("/staff/call")
def call_next():
    service_id = request.form.get("service_id", type=int)
    slot_value = request.form.get("slot", "")
    stmt = (db.select(Ticket)
            .join(AppointmentSlot)
            .where(Ticket.status == "waiting")
            .order_by(AppointmentSlot.start_time, Ticket.created_at)
            .limit(1))
    if service_id:
        stmt = stmt.where(Ticket.service_id == service_id)
    if slot_value:
        try:
            stmt = stmt.where(AppointmentSlot.start_time == time.fromisoformat(slot_value))
        except ValueError:
            pass  # ignore a slot value that is not a time
    t = db.session.scalar(stmt)
    if t is None:
        flash("No tickets waiting in queue.", "info")
    else:
        t.status = "called"
        t.called_at = func.now()
        db.session.commit()
        flash(f"Called Ticket #{t.id} ({t.user.name}).", "success")
    return redirect(url_for("staff_dashboard", service_id=service_id or None,
                            slot=slot_value or None))



STAFF_ACTIONS = {"call": "called", "serve": "served", "no-show": "no-show"}


@app.post("/staff/tickets/<int:ticket_id>/<action>")
def staff_action(ticket_id, action):
    new_status = STAFF_ACTIONS.get(action)
    if new_status is None:
        abort(404)
    t = db.get_or_404(Ticket, ticket_id)
    t.status = new_status
    if new_status == "called":
        t.called_at = func.now()  # the database fills in the time
    db.session.commit()
    flash(f"Ticket #{ticket_id} marked {new_status}.", "info")
    return redirect(url_for("staff_dashboard"))

@app.post("/staff/tickets/<int:ticket_id>/delete")
def delete_ticket(ticket_id):
    t = db.get_or_404(Ticket, ticket_id)
    db.session.delete(t)  # hard delete: the row is gone for good
    db.session.commit()
    flash(f"Ticket #{ticket_id} was deleted.", "warning")
    return redirect(url_for("staff_dashboard"))

@app.get("/staff/services")
def services_list():
    return render_template("services.html", services=all_services())


@app.post("/staff/services")
def service_create():
    name = request.form.get("name", "").strip()
    minutes = request.form.get("avg_minutes", type=int)
    if not name or len(name) > 60 or not minutes or minutes <= 0:
        flash("Enter a name (up to 60 characters) and minutes greater than 0.", "danger")
        return redirect(url_for("services_list"))
    db.session.add(Service(name=name, avg_minutes=minutes))
    try:
        db.session.commit()
        flash(f"Service '{name}' added.", "success")
    except IntegrityError:
        db.session.rollback()
        flash(f"A service named '{name}' already exists.", "danger")
    return redirect(url_for("services_list"))


@app.post("/staff/services/<int:service_id>")
def service_edit(service_id):
    s = db.get_or_404(Service, service_id)
    name = request.form.get("name", "").strip()
    minutes = request.form.get("avg_minutes", type=int)
    if not name or len(name) > 60 or not minutes or minutes <= 0:
        flash("Enter a name (up to 60 characters) and minutes greater than 0.", "danger")
        return redirect(url_for("services_list"))
    s.name = name
    s.avg_minutes = minutes
    s.active = request.form.get("active") == "on"  # an unticked box is not sent at all
    try:
        db.session.commit()
        flash(f"Service '{name}' updated.", "success")
    except IntegrityError:
        db.session.rollback()
        flash(f"A service named '{name}' already exists.", "danger")
    return redirect(url_for("services_list"))


@app.post("/staff/services/<int:service_id>/delete")
def service_delete(service_id):
    s = db.get_or_404(Service, service_id)
    name = s.name
    if s.tickets:
        flash(f"'{name}' has tickets, so it cannot be deleted. Turn it off instead.", "danger")
        return redirect(url_for("services_list"))
    db.session.delete(s)
    db.session.commit()
    flash(f"Service '{name}' deleted.", "warning")
    return redirect(url_for("services_list"))


@app.get("/queue/<int:ticket_id>/status.json")
def ticket_status(ticket_id):
    t = db.get_or_404(Ticket, ticket_id)
    return {"status": t.status, "ahead": people_ahead(t)}


@app.route("/hello")
def hello():
    # The plain-string version from the Routes slide.
    return "Hello, CCC181!"

@app.cli.command("seed")
def seed():
    """Add the starting services if they are not there yet."""
    starting = [
        ("New passport application", 10),
        ("Passport renewal", 10),
        ("Passport claiming", 10),
    ]
    for name, minutes in starting:
        exists = db.session.scalar(db.select(Service).filter_by(name=name))
        if exists is None:
            db.session.add(Service(name=name, avg_minutes=minutes))
    slots = [(time(9), time(11)), (time(11), time(13)),
             (time(13), time(15)), (time(15), time(17))]
    for start, end in slots:
        exists = db.session.scalar(db.select(AppointmentSlot).filter_by(start_time=start))
        if exists is None:
            db.session.add(AppointmentSlot(start_time=start, end_time=end))
    db.session.commit()
    print("Services and slots are ready.")


if __name__ == "__main__":
    # Lets you also start the app with: python app.py
    app.run(debug=True)