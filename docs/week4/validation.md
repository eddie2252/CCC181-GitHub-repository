# Validation


## Flask layer (curl, skipping the form)

| Rule | Layer | How I tested it | What happened |
| --- | --- | --- | --- |
| Name, email and service are all checked | Flask | `curl.exe -i -X POST /join -d "name=" -d "email=not-an-email" -d "service_id=999"` | `HTTP/1.1 400 BAD REQUEST`, nothing saved |
| Name is at most 80 characters | Flask | Same request with a 200-character name and otherwise valid fields | `HTTP/1.1 400 BAD REQUEST`, nothing saved |
| The appointment slot must exist | Flask | Same request with `appointment_time=99:99` | `HTTP/1.1 400 BAD REQUEST`, nothing saved |
| A switched-off service cannot be chosen | Flask | Switched off "New passport application" in Manage services, then sent a join for `service_id=1` | `HTTP/1.1 400 BAD REQUEST`, nothing saved |

## Database layer (psql, skipping Flask)

| Rule | Layer | How I tested it | What happened |
| --- | --- | --- | --- |
| A ticket needs a real service (FOREIGN KEY) | Database | `INSERT INTO tickets (user_id, service_id, appointment_slot_id) VALUES (1, 999, 1);` | `ERROR:  insert or update on table "tickets" violates foreign key constraint "tickets_service_id_fkey"` / `DETAIL:  Key (service_id)=(999) is not present in table "services".` |
| Status must be one of five values (CHECK) | Database | `UPDATE tickets SET status = 'lost' WHERE id = 1;` | `ERROR:  new row for relation "tickets" violates check constraint "ck_tickets_status"` |
| One account per email (UNIQUE) | Database | `INSERT INTO users (name, email) VALUES ('Copy', '...');` with an email that already exists | `ERROR:  duplicate key value violates unique constraint "users_email_key"` / `DETAIL:  Key (email)=(...) already exists.` |
| Average minutes must be above 0 (CHECK) | Database | `INSERT INTO services (name, avg_minutes) VALUES ('Test', 0);` | `ERROR:  new row for relation "services" violates check constraint "ck_services_avg_minutes"` |
| A service with tickets cannot be deleted (RESTRICT) | Database | `DELETE FROM services WHERE id = 1;` | `ERROR:  update or delete on table "services" violates foreign key constraint "tickets_service_id_fkey" on table "tickets"` / `DETAIL:  Key (id)=(1) is still referenced from table "tickets".` |
| A user needs an email (NOT NULL) | Database | `INSERT INTO users (name) VALUES ('No Email');` | `ERROR:  null value in column "email" of relation "users" violates not-null constraint` |
| A ticket needs an appointment slot (NOT NULL) | Database | `INSERT INTO tickets (user_id, service_id) VALUES (1, 1);` | `ERROR:  null value in column "appointment_slot_id" of relation "tickets" violates not-null constraint` |
| One open ticket per person and service (partial UNIQUE index) | Database | `INSERT INTO tickets (user_id, service_id, appointment_slot_id) VALUES (1, 1, 2);` while user 1 already had a waiting ticket for service 1 | `ERROR:  duplicate key value violates unique constraint "uq_tickets_one_open_per_service"` / `DETAIL:  Key (user_id, service_id)=(1, 1) already exists.` |

## A good row, to see the defaults

```sql
INSERT INTO tickets (user_id, service_id, appointment_slot_id) VALUES (1, 3, 1) RETURNING id, status, created_at;
```

Result: `id 26`, `status waiting`, `created_at 2026-11-08 19:08:35.85231+00`. I typed neither the status nor the time. The database filled in the defaults. I deleted this test ticket afterwards.

## No SQL built by hand

```
git grep -nE 'f["''].*(SELECT|INSERT|UPDATE|DELETE)' -- "*.py"
```

Result: no output. The code never builds SQL from user input, because SQLAlchemy sends values separately from the SQL.

## Most useful error

`uq_tickets_one_open_per_service`. It showed that the database stops a double tap even if Flask and the browser are skipped.