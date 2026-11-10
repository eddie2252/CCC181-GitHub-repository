# Persistence Verification (Part 11)

## 11a. Server & Database Restart Test

### Test Procedure
1. Created 5 new tickets across multiple services (`New passport application`, `Passport claiming`) the other are old ones from experimental phase.
2. Performed staff actions on tickets:
   - Called ticket `#31`
   - Marked ticket `#33` as served
   - Soft deleted ticket `#32` by marking status as `left` via the My Place page
3. Captured "Before Restart" state:
   - **Staff Dashboard:** Displayed waiting ticket `#29`, waiting `#30`, and called `#31`.
   - **SQL Query (`SELECT id, status, service_id, created_at FROM tickets ORDER BY id;`):** Returned 12 rows with exact statuses and timestamps.
4. Stopped Flask (`Ctrl+C`) and shut down Docker Compose containers (`docker compose down`). Verified no containers running (`docker compose ps`).
5. Restarted Docker containers (`docker compose up -d`) and verified `healthy` status. Restarted Flask application (`flask --app app run --debug`).
6. Captured "After Restart" state.

### Results & Verification
- **Dashboard:** `![Staff Dashboard After Restart](screenshots/restart-staff-after.png)` matches `![Staff Dashboard Before Restart](screenshots/restart-staff-before.png)` exactly.
- **SQL Records:** `![SQL Query After Restart](screenshots/restart-sql-after.png)` matches `![SQL Query Before Restart](screenshots/restart-sql-before.png)` exactly.
- **NFR-01 Verification:** **PASSED.** Zero tickets, statuses, or timestamps were lost during full server and database container restart.

---

## 11b. Rebuild From Scratch Test

### Procedure
Executed complete database reset using migrations and seeds:
1. `docker compose down -v` (Destroyed container and named volume `pgdata`)
2. `docker compose up -d` (Re-created clean database container)
3. `flask --app app db upgrade` (Re-created schema from migration history)
4. `flask --app app seed` (Populated initial services and appointment slots)

### Result
- Database schema rebuilt cleanly without relying on `db.create_all()`.
- Seed command inserted 3 active services and 4 appointment slots.
- Application loaded at `http://127.0.0.1:5000/join` showing active services in dropdown.
- Successfully submitted a new test ticket. Data persistence and migration scripts verified fully reproducible.