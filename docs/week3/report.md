# EDfly: Week 3 report

## 1. Title details
- **App:** EDfly, a passport-office queue system
- **Setting:** passport office
- **Name:** Eddie F. Castre Jr. · **Student ID:** 2024-0459 · **Section:** CCC181(CS3B) · **Date:** October 25, 2026
- **Pull request:** 

## 2. Personas

**Kijo Delavega, the person waiting.** 20, 3rd-year college student who commutes between campus and the consular site, using an Android phone with one hand. *"I booked my appointment online, but between classes and exams, I still don't know how long I'll wait or if I'm even in the right line."* Top tasks: join the queue with appointment details (FR-01), check live queue position and status (FR-02), leave the queue (FR-03).

**Elena Lamis, the staff member.** 42, senior consular officer at Counter Window 3, working on a desktop PC in a noisy hall. *"When the counter is full, I just need one button to call the next person and keep moving."* Top tasks: filter the queue by service (FR-04), call the next applicant (FR-05), mark Served or No-show (FR-06).

Full file: [personas.md](personas.md)

## 3. Screens


| Screenshot | Persona | Requirement IDs |
| --- | --- | --- |
| ![Join on a phone](screenshots/join-phone.png) | Kijo, on his phone | FR-01 |
| ![Join on a laptop](screenshots/join-laptop.png) | Kijo, on a laptop | FR-01 |
| ![My place on a phone](screenshots/myplace-phone.png) | Kijo, on his phone | FR-02, FR-03 |
| ![My place on a laptop](screenshots/myplace-laptop.png) | Kijo, on a laptop | FR-02, FR-03 |
| ![Staff on a phone](screenshots/staff-phone.png) | Elena (secondary device) | FR-04, FR-05, FR-06 |
| ![Staff on a laptop](screenshots/staff-laptop.png) | Elena, at her counter PC | FR-04, FR-05, FR-06 |

## 4. Design decisions

1. **The ticket number and status are the largest, highest-contrast elements on My place.** Because Kijo checks his phone outside in bright sunlight (Kijo, rule 2), his number, position and status must be easy to read at a glance.
2. **"Call next ticket" and the service filter sit at the top of the staff dashboard, and staff actions use POST with a flash message.** Because Elena alternates between paper forms and the screen, and handles one service per shift (Elena, rules 2 and 3), the main controls must be easy to reach and safe from accidental double-submits.
3. **All main buttons are at least about 44 px tall.** Because both Kijo (one-handed, carrying documents) and Elena (juggling paper forms) risk misclicks (Kijo and Elena, rule 1), I increased the button heights after the accessibility check.


## 5. Self-review
In my wireframe review ([feedback.md](feedback.md)) I found these main problems and changed the design:
- **Join:** no error state was drawn, and the date field was unclear. I added error text and a helper hint.
- **My place:** the wireframe showed "Current Number" instead of how many people are ahead of the user, and the appointment line was too prominent. I changed it to a "people ahead of you" sentence and made the appointment line smaller.
- **Staff:** on a phone the table cut off the Serve and No Show buttons. I kept the table scrolling inside its box and made the labels shorter.


## 6. Accessibility
Lighthouse accessibility (mobile): Join 99, My place 99, Staff 99. The most important issue I fixed was button size: Serve, No Show, Call next and Get a ticket were under about 44 px tall, so I increased them. Details: [accessibility.md](accessibility.md)

## 7. Usability test
My sister, an adult who has been through the passport process, tried the app on my desktop at laptop and phone width. She finished the tasks in about 1 to 2 minutes. She said it is easy to use and convenient for people who want to save time, but that it may be harder for older people who are not used to digital forms. The most serious problem: she asked why the form needed an appointment date when only today is accepted. I removed the date field, and the form now shows "today" as text next to the time. Before and after screenshots and the full notes are in [usability-test.md](usability-test.md).


## 8. Reflection
- **Hardest this week:** while building the queue app I realized that a person can join the line for any appointment time, so someone with a 3:00 PM slot can line up before the 9:00 AM people. This confused me because the slot should control the order, but the ticket number still decides it. To handle it, I added an appointment-slot filter on the staff dashboard so staff can call only the people in the slot they are serving. The limitation is that My place does not show the person's place within their own slot.
- **For Week 4 (database): What I will Change**
  - **Count by slot as well as service.** I will store the slot with each ticket, count people ahead by service and slot, and order by slot and then ticket number.
  - **Reject joining too early.** The server will check that the chosen slot has not passed and not let a person join far ahead of their time. 
  - **Update the status badge color live.** Right now the live update changes only the badge text, and the color updates on reload, which Kijo's scenario promises.
  - **Make it easier for older or less technical people.** After my sister tested the app, I realized it is inconvenient for elderly people who are not tech-savvy and who are used to asking the guard for information. Which I don’t have a solution yet. One idea to explore is letting the guard or staff register a person at the counter.


## 9. Declaration
I used Claude for step-by-step guidance on Parts 0 to 10, a rough sketch on whats my idea gonna look like in wireframes, ask questions where i am confused what am i doing right now, and clarification if this idea is valid or will contradicts to the point.