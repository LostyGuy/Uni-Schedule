from sqlalchemy import Boolean, String, Integer, Float, TIMESTAMP ,Column, ForeignKey
from sqlalchemy.orm import relationship
from backend.connection.connection import Base
from backend.timestamps import current_time

class user(Base):
    __tablename__ = 'user'
    userId: int = Column(
        Integer,
        primary_key= True,
        nullable= False,
        autoincrement= True,
    )
    username: str = Column(
        String,
        nullable= False,
    )
    name: str = Column(
        String,
        nullable= False,
    )
    surname: str = Column(
        String,
        nullable= False,
    )
    email: str = Column(
        String,
        nullable= False,
    )
    hashed_password: str = Column(
        String,
        nullable= False,
    )
    roleId: int = Column(
        Integer,
        ForeignKey("roles.roleId"),
        nullable= False,
    )
    is_active: bool = Column(
        Boolean,
        nullable= True,
    )
    last_active: TIMESTAMP = Column(
        TIMESTAMP,
        nullable= True,
    )
    created_at: TIMESTAMP = Column(
        TIMESTAMP,
        nullable= False,
    )
    
class schedule(Base):
    __tablename__ = 'schedule'
    scheduleId: int = Column(
        Integer,
        primary_key= True,
        nullable= False,
        autoincrement= True,
    )
    name: String = Column(
        String,
        nullable= False,
    )
    description: str = Column(
        String,
    )
    status: bool = Column(
        Boolean,
        nullable= False,
        default= 'Active'
    )
    groupId: int = Column(
        Integer,
        nullable= True,
    )
    created_by: int = Column(
        Integer,
        ForeignKey("user_login_credentials.id_user"),
        nullable= False,
    )
    created_at: str = Column(
        TIMESTAMP,
        nullable= False,
    )
    updated_at: str = Column(
        TIMESTAMP,
        nullable= False,
    )
    
# TODO: Recurring Events
class events(Base):
    __tablename__ = 'events'
    eventid: int = Column(
        Integer,
        primary_key= True,
        nullable= False,
        autoincrement= True,
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
        autoincrement= True,
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
        autoincrement= True,
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
        autoincrement= True,
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
        ForeignKey("role.role_id"),
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
        autoincrement= True,
    )
    name: str = Column(
        String,
        nullable= False,
    )
    hex_value: str = Column(
        String,
        nullable= False,
    )

class roles(Base):
    __tablename__ = 'roles'
    role_id: int = Column(
        Integer,
        primary_key= True,
        nullable= False,
        autoincrement= True,
    )
    name: str = Column(
        String,
        nullable= False,
    )
    description: str = Column(
        String,
        nullable= True,
    )

class login_session(Base):
    __tablename__ = 'login_session'
    
    id: int = Column(
        Integer,
        autoincrement= True,
        nullable= False,
        primary_key= True,
        unique= True
    )
    user_id: int = Column(
        Integer,
        ForeignKey('user_login_credentials.id_user'),
        nullable= False,
        index= True,
    )
    access_token: str = Column(
        String,
        nullable= False,
    )
    issued_at: TIMESTAMP = Column(
        TIMESTAMP,
        nullable= False,
    )
    valid_till: str = Column(
        String,
        nullable= False,
    )
    issued_from_endpoint: str = Column(
        String,
        nullable= False,
    )
    valid_for_endpoint: str = Column(
        String,
        nullable= False,
    )
    status: str = Column(
        String,
        nullable= False,
        default= 'Active',
    )
    jwt_id: str = Column(
        String,
        nullable= False,
    )
    created_at: TIMESTAMP = Column(
        TIMESTAMP,
        nullable= False,
        default= current_time(),
    )