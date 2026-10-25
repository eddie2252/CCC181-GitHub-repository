# Week 3 Wireframe & Persona Self-Review

## Screen 1: Join the Queue (`/join`)

* **Works well:** The form follows the order a person thinks in (name, email, service, then when), and "Get a ticket" is one wide button at the bottom. allows Kijo to quickly enter ticket with one thumb
* **Problem (Error Prevention):** The frames show no error state, and the date is 2026-10-26, which is not today. The server rule says the appointment date must be today, so a first-time user can't tell why a date would be rejected (error prevention). The Appointment Time dropdown also has no hint about which slots are valid.
* **Change:** Add a short helper line under Appointment Date ("Today only") and draw one error message under the date field, e.g. "Appointment date must be today." Change the sample date in both frames to today's date.

---

## Screen 2: My Place (`/queue/<id>`)

* **Works well:** The ticket number (#2) is prominently displayed in ultra-large bold text at the top of the card, allowing Kijo to check his ticket status at a single glance under bright sunlight.
* **Problem (Visibility of System Status):** There is no position sentence. It only shows "Current Number: 1", so Kijo has to work out how many people are ahead of her (recognition rather than recall). The appointment line is also as big as the service line, and the gray "Waiting" text is low contrast on the gray card.
* **Change:** Replace "Current Number" with "1 person ahead of you" ("You're next!" when 0). Make the appointment line small text under the service name. Darken the status text, or put it in a badge.


---

## Screen 3: Staff Dashboard (`/staff`)

* **Works well:** The primary "CALL NEXT TICKET" button is placed at the top next to the service filter dropdown, making Elena's most repeated action instantly accessible without scanning individual table rows.
* **Problem (Recognition rather than Recall / Error Prevention):** On the phone the table cuts off at Status, so the Serve and No Show buttons are off-screen until you scroll sideways. "Application" also breaks mid-word ("Applicat-ion"). Both hurt the match with the real world, since staff expect to see the action next to the name.
* **Change:** Keep the sideways scroll inside the box , but add a scroll hint such as "← swipe →". widen that column so it doesn't break mid-word.
