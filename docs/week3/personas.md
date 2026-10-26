# Week 3 Personas: Passport Queue App

## Kijo Delavega, the person waiting

> "I booked my appointment online, but between classes and exams, I still don't know how long I'll wait or if I'm even in the right line."

| | |
| --- | --- |
| **Photo or sketch** | ![Kijo Delavega](screenshots/KijoDelavega.png) |
| **Age, role and background** | 20, 3rd-year college student, attending lectures and commuting between campus and the consular site  |
| **Goals** | 1. Obtain a passport as a primary government ID and prepare early for post-graduation overseas nursing requirements. 2. Monitor his queue position remotely so he doesn't have to wait in a crowded lobby during study hours.<3. Reach the counter window right on time without missing his afternoon lecture or clinical endorsement.|
| **Frustrations** | 	1. Standing in a crowded hall without knowing if this is the right counter.  2. Not being sure which of the forms and counters apply to him.  3. Missing his priority number being called because the hall is noisy. |
| **Devices and context** | Mid-range Android phone, used with one hand while the other holds his documents and bag. Mobile data is slow inside the building. | |
| **Tech comfort** | Medium — comfortable with browser-based, he uses Facebook and messaging apps |
| **Accessibility needs** | Needs large target areas and explicit visual boundaries for action buttons to avoid misclicks when juggling physical documents and Strong Mobile Data Connection |

### Scenario

Kijo arrives near the consular service office at 10:15 AM during a 2-hour break between his morning lecture and 1:00 PM exam review. He opens the app on his phone, enters his details for "Passport renewal", and gets ticket #2. Because the indoor waiting area is loud and crowded, he steps out to a nearby shaded bench to review his exam notes. He keeps the "My place" page open on his phone screen to track how many people are ahead of him. When his status updates to "Called" with a bright badge color change, he walks straight to the window, presents his documents, and finishes with plenty of time to head back to campus.

### Top tasks in the app

| Task | Screen | Requirement ID |
| --- | --- | --- |
| Join the queue with appointment details | Join | FR-01 |
| Check live queue position and status | My place | FR-02 |
| Leave the queue if pulled into an urgent class re-scheduling | My place | FR-03 |

### What this means for my interface

1. Because Kijo uses his phone single-handed while carrying folders or a backpack, all primary buttons and form controls must have large, easy-to-tap touch targets.
2. Because he checks his status while sitting or walking outside under bright sunlight, ticket numbers, position counts, and status badges must use large, high-contrast typography.
3. Because his schedule is tightly bound to class times, the My place page must clearly display the exact count of people ahead so he knows precisely when to walk back to the counter window.


---

## Elena Lamis, the staff member

> "When the counter is full, I just need one button to call the next person and keep moving." 

| | |
| --- | --- |
| **Photo or sketch** | ![Elena Lamis](screenshots/ElenaLamis.png)|
| **Age, role and background** | 42, Senior Consular Officer, handling passport renewals and claim processing at Window 3 for 8 hours daily |
| **Goals** | 1. See who is next in line without asking around. 2. Call and serve people with as few clicks as possible. 3. Handle one type of service at a time (new, renewal or claiming).
| **Frustrations** | 1. Applicants walk up not knowing if they are in the right line. 2. People who don't come when called slow the whole queue. 3. Cluttered or high-density software tables that lead to misclicks when switching focus between physical paper forms and screen controls |
| **Devices and context** | Desktop PC with a 24-inch monitor and mouse at Counter Window 3, operated in a high-traffic, noisy hall |
| **Tech comfort** | Medium — comfortable with browser-based administrative portals and office software |
| **Accessibility needs** | Needs large target areas and explicit visual boundaries for action buttons to avoid misclicks while juggling physical passport applications |

### Scenario

Elena logs into her workstation at Counter Window 3, assigned to handle passport renewal processing for the morning shift. She opens the staff dashboard and filters the list to display only "Passport renewal" tickets. As she completes document verification for ticket #1, she clicks "Call next" to call ticket #2. The dashboard updates instantly to reflect ticket #2 as "Called". Once Kijo presents his requirements at the window, Elena verifies his forms and clicks "Serve" to finalize the transaction, keeping the queue moving smoothly without calling out names verbally into the hall.

### Top tasks in the app

| Task | Screen | Requirement ID |
| --- | --- | --- |
| Filter waiting queue by passport service category | Staff dashboard | FR-04 |
| Call the next waiting applicant in line | Staff dashboard | FR-05 |
| Mark applicant status as Served or No-show | Staff dashboard | FR-06 |

### What this means for my interface

1. Because Elena rapidly alternates between physically checking passport application documents and clicking screen controls, action buttons (Call next, Serve, No-show) must have large touch targets, generous spacing, and distinct color schemes.
2. Because her counter window handles specific services during her shift, service filtering controls must be located prominently at the top of the staff dashboard.
3. Because status modifications must be clear and immune to accidental double-submits, staff actions must send POST requests and trigger clear flash feedback messages at the top of the dashboard.