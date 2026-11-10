# EDfly requirements

**Setting:** Passport office, weekday appointments in four 2-hour slots (9-11, 11-1, 1-3, 3-5)
**People who wait:** Applicants renewing or applying for a passport, e.g. Kijo Delavega in [docs/week3/personas.md](week3/personas.md)
**People who serve:** Counter staff, e.g. Elena Lamis in [docs/week3/personas.md](week3/personas.md)

**Problem statement:** An applicant with a passport appointment needs a way to see how many people are ahead of them without standing in a crowded hall, because they miss their turn whenever they step out.

## Functional requirements

| ID | Requirement | Priority | Stores data? | Status |
| --- | --- | --- | --- | --- |
| FR-01 | An applicant can join the queue for a passport service by entering their name and email and choosing the appointment slot they already booked online.| Must | **Yes** | Built (Week 3) |
| FR-02 | An applicant can see their ticket number, status, and how many people are ahead of them. | Must | **Yes** | Built (Week 3) |  
| FR-03 | An applicant can leave the queue before being called. | Must | **Yes** | Built (Week 3) |
| FR-04 | A staff member can filter the waiting list by passport service. | Must | **Yes** | Built (Week 3) |
| FR-05 | A staff member can call the next waiting ticket. | Must | **Yes** | Built (Week 3) |
| FR-06 | A staff member can mark a called ticket as served or no-show. | Must | **Yes** | Built (Week 3) |
| FR-07 ★ | A staff member can see each ticket's appointment slot and filter the list by slot. | Should | **Yes** | Built (Week 3) |
| FR-08 | A staff member can add, rename and switch off a passport service. | Must | **Yes** | This week |
| FR-09 | A staff member can delete a ticket that was created by mistake. | Should | **Yes** | This week |
| FR-10 ★ | A senior citizen or person with a disability can join a priority lane that is served first. | Should | **Yes** | Later |
| FR-11 ★ | An applicant is told which counter window to go to when their ticket is called. | Should | **Yes** | Later |
| FR-12 | A staff member can see how many people left before being served, per service, per day. | Should | **Yes** | Later |
| FR-13 | An applicant can switch the page to a larger text size. | Could | No | Later |
| FR-14 | An applicant is clearly alerted on My place when their ticket is called (the badge colour and a message change, without a reload). | Should | No | Later |



## Non-functional requirements

| ID | Requirement | Category | Priority |
| --- | --- | --- | --- |
| NFR-01 | No ticket is lost when the server or the database restarts. | Reliability | Must |
| NFR-02 | Two people can never get the same ticket number, even if they join at the same moment. | Data integrity | Must |
| NFR-03 | My place loads in under 2 seconds on mobile data. | Performance | Should |
| NFR-04 | Every screen scores 90 or higher in the Lighthouse accessibility check (Week 3: 99 on all three). | Accessibility | Must |
| NFR-05 | The database password is never stored in the repository. | Security | Must |
| NFR-06 | My place shows a status change within 10 seconds of a staff action, without a reload. | Usability | Should |

## MVP

**MVP:** FR-01, FR-02, FR-03, FR-04, FR-05, FR-06, FR-08, NFR-01, NFR-02, NFR-04, NFR-05. This is the smallest version that still solves the problem: an applicant can join, see their place and leave, staff can call and finish tickets and manage the services, and nothing is lost when the system restarts.

**Out of scope (this semester):**
- **SMS or email alerts when a ticket is called.** They need a paid or external messaging service, and the live status on My place already covers the need.
- **Online payment and document upload.** These belong to the real passport application, not the queue, and they raise privacy and security risks I can't handle yet.
- **Several branches or offices.** The app is built for one office, and supporting more would change the schema.
- **Booking appointments.** The passport website already does this; EDfly only manages the line on the day.

## Feedback from a real person

| Who (role only, no full name) | What they said | What I changed |
| --- | --- | --- |
| Passport applicant (has been through the process) | Something is missing: the number of people ahead did not seem to change as she got closer, and when she was called she could not notice it right away because only the text changed. | Added FR-14: a clear alert (colour and message) when a ticket is called. |
| Passport applicant | Nothing seemed wrong, but the app felt like it was lacking in that area. | Kept the list as it is; FR-14 covers the gap. |
| Passport applicant | Her top three: seeing her position in line, noticing right away when she is called, and convenience or easy access. | Kept FR-02 and FR-01 as Must; FR-14 now covers "noticing right away". |