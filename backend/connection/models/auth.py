from sqlalchemy import Column, BigInteger, String, Boolean, DateTime, ForeignKey, func

from backend.connection.connection import Base

class Role(Base):
    __tablename__ = "roles"

    role_id = Column(
        BigInteger,
        primary_key= True,
        nullable= False,
        autoincrement= True,
    )
    name = Column(
        String,
        nullable= False,
    )
    description = Column(
        String,
        nullable= True,
    )
    can_manage_events = Column(
        Boolean,
        nullable= True,
    )
    can_invite_members = Column(
        Boolean,
        nullable= True,
    )
    created_at = Column(
        DateTime(timezone= True),
        nullable= False,
        server_default= func.now(),
    )
