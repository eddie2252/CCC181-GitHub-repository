from datetime import datetime, time

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (
    CheckConstraint, DateTime, ForeignKey, Index, String, Time, func, text, true,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80))
    email: Mapped[str] = mapped_column(String(120), unique=True)
    role: Mapped[str] = mapped_column(String(20), default="visitor", server_default="visitor")

    tickets: Mapped[list["Ticket"]] = relationship(back_populates="user")

    __table_args__ = (
        CheckConstraint("role IN ('visitor', 'staff')", name="ck_users_role"),
    )


class Service(db.Model):
    __tablename__ = "services"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(60), unique=True)
    avg_minutes: Mapped[int] = mapped_column(default=10, server_default="10")
    active: Mapped[bool] = mapped_column(default=True, server_default=true())

    tickets: Mapped[list["Ticket"]] = relationship(back_populates="service")

    __table_args__ = (
        CheckConstraint("avg_minutes > 0", name="ck_services_avg_minutes"),
    )


class AppointmentSlot(db.Model):
    __tablename__ = "appointment_slots"

    id: Mapped[int] = mapped_column(primary_key=True)
    start_time: Mapped[time] = mapped_column(Time, unique=True)
    end_time: Mapped[time] = mapped_column(Time)

    tickets: Mapped[list["Ticket"]] = relationship(back_populates="appointment_slot")

    __table_args__ = (
        CheckConstraint("end_time > start_time", name="ck_appointment_slots_end_after_start"),
    )


class Ticket(db.Model):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[str] = mapped_column(String(20), default="waiting", server_default="waiting")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    called_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"))
    service_id: Mapped[int] = mapped_column(ForeignKey("services.id", ondelete="RESTRICT"))
    appointment_slot_id: Mapped[int] = mapped_column(
        ForeignKey("appointment_slots.id", ondelete="RESTRICT")
    )

    user: Mapped["User"] = relationship(back_populates="tickets")
    service: Mapped["Service"] = relationship(back_populates="tickets")
    appointment_slot: Mapped["AppointmentSlot"] = relationship(back_populates="tickets")

    __table_args__ = (
        CheckConstraint(
            "status IN ('waiting', 'called', 'served', 'no-show', 'left')",
            name="ck_tickets_status",
        ),
        Index(
            "uq_tickets_one_open_per_service",
            "user_id",
            "service_id",
            unique=True,
            postgresql_where=text("status IN ('waiting', 'called')"),
        ),
    )