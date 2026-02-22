from sqlalchemy import Boolean, String, Integer, Float, TIMESTAMP ,Column, ForeignKey
from sqlalchemy.orm import relationship
from backend.db import Base

class user_login_credentials(Base):
    __tablename__ = 'user_login_credentials'
    id: int = Column(
        Integer,
        primary_key= True,
        nullable= False,
        autoincrement= True,
        unique= True,
        default= '0',
    )
    email: str = Column(
        String,
        nullable= False,
    )
    hashed_password: str = Column(
        String,
        nullable= False,
    )
    created_at: TIMESTAMP = Column(
        TIMESTAMP,
        nullable= False,
    )
    policy_agreement: bool = Column(
        Boolean,
        nullable= False,
    )
    lastly_signed_in_on: TIMESTAMP = Column(
        TIMESTAMP,
        nullable= False,
    )
    role: int = Column(
        Integer,
        ForeignKey("role.id"),
        nullable= False,
    )

class schedule(Base):
    __tablename__ = 'schedule'
    id: int = Column(
        Integer,
        primary_key= True,
        nullable= False,
        unique= True,
    )
    title: String = Column(
        String,
        nullable= False,
    )
    description: str = Column(
        String,
    )
    created_by: int = Column(
        Integer,
        ForeignKey("user_login_credentials.id"),
        nullable= False,
    )
    created_at: str = Column(
        TIMESTAMP,
        nullable= False,
    )
    last_update_at: str = Column(
        TIMESTAMP,
        nullable= False,
    )

# TODO: Recurring Events
class event(Base):
    __tablename__ = 'event'
    id: int = Column(
        Integer,
        primary_key= True,
        nullable= False,
        unique= True,
    )
    title: str = Column(
        String,
        nullable= False,
    )
    description: set = Column(
        String,
        nullable= True,
    )
    from_time = ...
    to_time = ...
    from_date = ...
    to_date = ...
    entire_day: bool = Column(
        Boolean,
        nullable= True,
    )
    color: int = Column(
        Integer,
        ForeignKey("color.id"),
        nullable= False,
    )
    location: str = Column(
        String,
        nullable= True,
    )
    last_update_at: str = Column(
        TIMESTAMP,
        nullable= False,
    )
    created_by: int = Column(
        Integer,
        ForeignKey("user_login_credentials.id"),
        nullable= False,
    )
    created_at: str = Column(
        TIMESTAMP,
        nullable= False,
    )

class event_exception(Base):
    __tablename__ = 'event_exception'
    id: int = Column(
        Integer,
        primary_key= True,
        nullable= False,
        unique= True,
    )
    new_title: str = Column(
        String,
        nullable= False,
    )
    new_description: set = Column(
        String,
        nullable= True,
    )
    new_from_time = ...
    new_to_time = ...
    new_from_date = ...
    new_to_date = ...
    new_entire_day: bool = Column(
        Boolean,
        nullable= True,
    )
    new_color: int = Column(
        Integer,
        ForeignKey("color.id"),
        nullable= False,
    )
    new_location: str = Column(
        String,
        nullable= True,
    )
    last_update_at: str = Column(
        TIMESTAMP,
        nullable= False,
    )
    created_by: int = Column(
        Integer,
        ForeignKey("user_login_credentials.id"),
        nullable= False,
    )
    created_at: str = Column(
        TIMESTAMP,
        nullable= False,
    )

class schedule_events(Base):
    __tablename__ = 'schedule_events'
    id: int = Column(
        Integer,
        primary_key= True,
        nullable= False,
        unique= True,
    )
    id_schedule: int = Column(
        Integer,
        ForeignKey("schedule.id"),
        nullable= False,
    )
    id_event: int = Column(
        Integer,
        ForeignKey("event.id"),
        nullable= False,
    )
    created_at: str = Column(
        TIMESTAMP,
        nullable= False,
    )

class schedule_participants(Base):
    __tablename__ = 'schedule_participants'
    id: int = Column(
        Integer,
        primary_key= True,
        nullable= False,
        unique= True,
    )
    id_schedule: int = Column(
        Integer,
        ForeignKey("schedule.id"),
        nullable= False,
    )
    id_user: int = Column(
        Integer,
        ForeignKey("user_login_credentials.id"),
        nullable= False,
    )
    role: str = Column(
        Integer,
        ForeignKey("role.id"),
        nullable= False,
    )
    created_at: str = Column(
        TIMESTAMP,
        nullable= False,
    )

class color(Base):
    __tablename__ = 'color'
    id: int = Column(
        Integer,
        primary_key= True,
        nullable= False,
        unique= True,
    )
    name: str = Column(
        String,
        nullable= False,
    )
    hex_value: str = Column(
        String,
        nullable= False,
    )

class role(Base):
    __tablename__ = 'role'
    id: int = Column(
        Integer,
        primary_key= True,
        nullable= False,
        unique= True,
    )
    name: str = Column(
        String,
        nullable= False,
    )
    description: str = Column(
        String,
        nullable= True,
    )

