"""CCC181 Week 2: a "Hello, Flask" starter app.

Run it with:
    flask --app app run --debug
then open http://127.0.0.1:5000
"""

from datetime import date
from flask import Flask, abort, flash, redirect, render_template, request, url_for
app = Flask(__name__)
app.secret_key = "dev-only-change-me" 


SERVICES = [
    {"id": 1, "name": "New passport application"},
    {"id": 2, "name": "Passport renewal"},
    {"id": 3, "name": "Passport claiming"},
]

APPOINTMENT_SLOTS = [
    {"value": "09:00", "label": "09:00 AM to 11:00 AM"},
    {"value": "11:00", "label": "11:00 AM to 01:00 PM"},
    {"value": "13:00", "label": "01:00 PM to 03:00 PM"},
    {"value": "15:00", "label": "03:00 PM to 05:00 PM"},
]


TICKETS = [
    {"number": 1, "name": "Raven Lamis", "email": "raven.lamis@example.com",
     "service_id": 1, "status": "waiting",
          "appointment_date": "2026-10-26", "appointment_time": "09:00"},
    {"number": 2, "name": "Kijo Delavega", "email": "kijo.delavega@example.com",
     "service_id": 2, "status": "waiting",
     "appointment_date": "2026-10-26", "appointment_time": "09:00"},
    {"number": 3, "name": "Winchester Cosning", "email": "winchester.cosning@example.com",
     "service_id": 3, "status": "waiting",
     "appointment_date": "2026-10-26", "appointment_time": "11:00"},
]


@app.route("/")
def index():
    # render_template looks inside the templates/ folder and passes
    # keyword arguments to the template as variables.
    return render_template("index.html", name="Ana", tickets=TICKETS)


@app.route('/queue/<int:ticket_id>')
@app.route('/ticket/<int:ticket_id>')
def ticket(ticket_id):
    ticket_item = next((t for t in TICKETS if t.get('number') == ticket_id or t.get('id') == ticket_id), None)
    if not ticket_item:
        abort(404)

    service = next((s for s in SERVICES if s['id'] == ticket_item['service_id']), None)
    service_name = service['name'] if service else "General Service"

    people_ahead = sum(
        1 for t in TICKETS 
        if t['service_id'] == ticket_item['service_id']
        and t['status'] == 'waiting' and t.get('number', 0) < ticket_id
    )

    slot = next((s for s in APPOINTMENT_SLOTS if s['value'] == ticket_item.get('appointment_time')), None)
    slot_label = slot['label'] if slot else ticket_item.get('appointment_time', '')

    return render_template(
        'ticket.html', 
        ticket=ticket_item, 
        service_name=service_name, 
        people_ahead=people_ahead,
        slot_label=slot_label
    )


@app.route('/queue/<int:ticket_id>/leave', methods=['POST'])
def leave_queue(ticket_id):
    ticket_item = next((t for t in TICKETS if t.get('number') == ticket_id or t.get('id') == ticket_id), None)
    if ticket_item and ticket_item['status'] in ['waiting', 'called']:
        ticket_item['status'] = 'no-show'
        flash("You have left the queue.", "info")
    return redirect(url_for('join_form'))


@app.get("/join")
def join_form():
    return render_template("join.html", services=SERVICES,
                           slots=APPOINTMENT_SLOTS, form={})


@app.post("/join")
def join():
    form = request.form
    name = form.get("name", "").strip()
    email = form.get("email", "").strip().lower()
    service_id = form.get("service_id", type=int)
    appointment_date = form.get("appointment_date", "").strip()
    appointment_time = form.get("appointment_time", "").strip()

    errors = {}
    if not name:
        errors["name"] = "Enter your name."
    if "@" not in email:
        errors["email"] = "Enter a valid email address."
    if service_id not in [s["id"] for s in SERVICES]:
        errors["service_id"] = "Choose a service."

    if not appointment_date:
        errors["appointment_date"] = "Choose your appointment date."
    else:
        try:
            if date.fromisoformat(appointment_date) != date.today():
                errors["appointment_date"] = "Appointment date must be today."
        except ValueError:
            errors["appointment_date"] = "Enter a valid date."

    if appointment_time not in [s["value"] for s in APPOINTMENT_SLOTS]:
        errors["appointment_time"] = "Choose an appointment time."

    if errors:
        flash("Please fix the highlighted fields.", "danger")
        return render_template("join.html", services=SERVICES,
                               slots=APPOINTMENT_SLOTS, form=form,
                               errors=errors), 400

    number = TICKETS[-1]["number"] + 1 if TICKETS else 1
    TICKETS.append({"number": number, "name": name, "email": email,
                    "service_id": service_id, "status": "waiting",
                    "appointment_date": appointment_date,
                    "appointment_time": appointment_time})
    flash(f"You joined the queue. Your ticket is #{number}.", "success")
    return redirect(url_for("ticket", ticket_id=number))


@app.route("/staff")
def staff_dashboard():
    service_filter = request.args.get("service_id", type=int)
    slot_filter = request.args.get("slot", "")
    
    filtered_tickets = [t for t in TICKETS if t["status"] in ("waiting", "called")]
    if service_filter:
        filtered_tickets = [t for t in filtered_tickets if t["service_id"] == service_filter]
    if slot_filter:
        filtered_tickets = [t for t in filtered_tickets if t["appointment_time"] == slot_filter]

    # Enrich tickets with human-readable service name and appointment slot label
    display_tickets = []
    for t in filtered_tickets:
        service = next((s for s in SERVICES if s["id"] == t["service_id"]), None)
        slot = next((s for s in APPOINTMENT_SLOTS if s["value"] == t.get("appointment_time")), None)
        display_tickets.append({
            **t,
            "service_name": service["name"] if service else "General Service",
            "slot_label": slot["label"] if slot else t.get("appointment_time", "")
        })

    return render_template(
        "staff.html", 
        tickets=display_tickets, 
        services=SERVICES, 
        selected_service=service_filter,
        slots=APPOINTMENT_SLOTS,
        selected_slot=slot_filter
    )


@app.post("/staff/call")
def call_next():
    service_filter = request.form.get("service_id", type=int)
    slot_filter = request.form.get("slot", "")
    
    # Find the first ticket waiting in line
    next_ticket = next(
        (t for t in TICKETS if t["status"] == "waiting" and (not service_filter or t["service_id"] == service_filter) and (not slot_filter or t["appointment_time"] == slot_filter)),
        None
    )
    if next_ticket:
        next_ticket["status"] = "called"
        ticket_num = next_ticket.get("number") or next_ticket.get("id")
        flash(f"Called Ticket #{ticket_num} ({next_ticket['name']}).", "success")
    else:
        flash("No tickets waiting in queue.", "info")
        
    return redirect(url_for("staff_dashboard", service_id=service_filter or None, slot=slot_filter or None))


@app.post("/staff/serve/<int:ticket_id>")
def mark_served(ticket_id):
    ticket_item = next((t for t in TICKETS if t.get("number") == ticket_id or t.get("id") == ticket_id), None)
    if ticket_item:
        ticket_item["status"] = "served"
        flash(f"Ticket #{ticket_id} marked as Served.", "success")
    return redirect(url_for("staff_dashboard"))


@app.post("/staff/noshow/<int:ticket_id>")
def mark_noshow(ticket_id):
    ticket_item = next((t for t in TICKETS if t.get("number") == ticket_id or t.get("id") == ticket_id), None)
    if ticket_item:
        ticket_item["status"] = "no-show"
        flash(f"Ticket #{ticket_id} marked as No-Show.", "warning")
    return redirect(url_for("staff_dashboard"))

@app.get("/queue/<int:ticket_id>/status.json")
def ticket_status(ticket_id):
    t = next((t for t in TICKETS if t["number"] == ticket_id), None)
    if t is None:
        abort(404)
    ahead = sum(1 for x in TICKETS
                if x["service_id"] == t["service_id"]
                and x["status"] == "waiting" and x["number"] < t["number"])
    return {"status": t["status"], "ahead": ahead}



@app.route("/hello")
def hello():
    # The plain-string version from the Routes slide.
    return "Hello, CCC181!"


if __name__ == "__main__":
    # Lets you also start the app with: python app.py
    app.run(debug=True)

