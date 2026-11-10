# Schema review

**Works well:** `tickets` stores only facts about one visit (`created_at`, `status`) and never a position, a count of people ahead or a waiting time. "Ahead" is computed as the number of `waiting` tickets for the same service that are in an earlier appointment slot, or in the same slot with an earlier `created_at`, so it cannot go stale when someone is called, leaves or is marked no-show. Found by question 3.
**Problem:** Nothing stopped a double tap on Join from creating two open tickets for the same person and service. The second ticket would count as another person "ahead" for everyone behind it, which breaks FR-02. Found by question 4.
**Change:** Added a partial unique index on `tickets (user_id, service_id)` where `status IN ('waiting', 'called')`, documented under 2c in `schema.md`. The ERD is unchanged, because dbdiagram cannot draw a partial index. `left` and `no-show` tickets are outside the index, so a person who left can join again.

---

**Works well:** All three foreign keys use `RESTRICT` on purpose. A service, slot or applicant that has tickets cannot be deleted, so old tickets stay available for the left-before-served report (FR-12). Staff switch a service off with `services.active` instead of deleting it. Found by question 5.
**Problem:** No requirement uses `services.avg_minutes`. FR-02 shows people ahead, not a waiting time. Found by question 1.
**Change:** Kept it. It is a fact about the service, it has a `CHECK (avg_minutes > 0)`, and it is needed if an estimated wait is added later. No requirement or ERD change.

---

**Works well:** Slot times are `time` columns, not text, with `CHECK (end_time > start_time)`, so a slot cannot end before it starts. Found by question 6.
**Problem:** `end_time` is always `start_time` plus 2 hours, so it could be computed instead of stored. Found by question 3.
**Change:** Kept it. The length of a slot is a fact about the slot, and storing it means the schema still works if a slot is ever 1 or 3 hours. No ERD change.