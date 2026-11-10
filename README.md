# CCC181-GitHub-repository

EDfly is a queue management system for a passport office, where people register an appointment online, get a schedule to fill up their forms, and later get a second schedule to claim their passport. On the day, they join the queue and see their ticket number, status and position, while staff call and serve tickets from a dashboard.

Requirements: [docs/requirements.md](docs/requirements.md)

## How to run it

You need Python, Git and Docker Desktop.

1. Create and activate a virtual environment: `python -m venv .venv`, then `.venv\Scripts\activate` on Windows.
2. Copy `.env.example` to `.env` and put your own password in both lines.
3. Start the database: `docker compose up -d` (wait until `docker compose ps` says healthy).
4. Install the packages: `pip install -r requirements.txt`
5. Create the tables: `flask --app app db upgrade`
6. Add the starting services and appointment slots: `flask --app app seed`
7. Start the app: `flask --app app run --debug`, then open http://127.0.0.1:5000

## Note

The staff pages (`/staff` and Manage services) have no login yet, so anyone can open them. Protecting them is planned for Week 11 (issue #4).