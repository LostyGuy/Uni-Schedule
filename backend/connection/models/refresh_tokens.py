from sqlalchemy import Column, BigInteger, String, DateTime, Boolean, ForeignKey, func, JSON, text

from backend.connection.connection import Base


class RefreshToken(Base):
    __tablename__ = 'refresh_tokens'
    user_session_id = Column(
        BigInteger,
        primary_key= True,
        nullable= False,
        autoincrement= True,
    )
    user_id = Column(
        BigInteger,
        ForeignKey("users.user_id"),
        nullable= False,
    )
    token_hash = Column(
        String,
        nullable= False,
    )
    expire_at = Column(
        DateTime(timezone= True),
        nullable= False,
    )
    is_revoked = Column(
        Boolean,
        nullable= False,
        server_default= text("false"),
    )
    is_active = Column(
        Boolean,
        nullable= False,
        server_default= text("false"),
    )
    device_name = Column(
        String,
        nullable= True,
        server_default= text("''"),
    )
    ip_address = Column(
        String,
        nullable= False,
    )
    last_used_at = Column(
        DateTime(timezone= True),
        nullable= False,
        server_default= func.now(),
    )
    created_at = Column(
        DateTime(timezone= True),
        nullable= False,
        server_default= func.now(),
    )
