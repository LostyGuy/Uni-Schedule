import os
import secrets

import jwt
from datetime import timedelta
from sqlalchemy import select, update

import backend.connection.models as models 
from backend.security.hashing import hash_string
from backend.timestamps import current_time
from backend.logging import current_function, log_info, log_error
from backend.config import get_environmental_variables

REFRESH_LIFESPAN = timedelta(days=30)
ACCESS_LIFESPAN = timedelta(minutes=15)

SECRET_KEY = get_environmental_variables("SECRET_KEY")
ALGORITHM = get_environmental_variables("ALGORITHM")

def create_refresh_token(user_id:int, device_name:str, ip_address: str, db_session) -> str | None:
    
    raw_token: str = secrets.token_urlsafe(64)
    token_hash: str = hash_string(raw_token)
    
    try:
        token = models.RefreshToken(
            user_id = user_id,
            token_hash = token_hash,
            expire_at = str(current_time() + REFRESH_LIFESPAN),
            device_name = device_name,
            ip_address = ip_address,
        )
        db_session.add(token)
        db_session.commit()
    except Exception as e:
        log_error("Create_Refresh_Token: ", e)
        return None
    
    return raw_token
    

def update_refresh_token(raw_token: str, db_session) -> str | None:
    
    token_hash: str = hash_string(raw_token)
    
    current_token = db_session.execute(
        select(models.RefreshToken).where(
            models.RefreshToken.token_hash == token_hash,
            models.RefreshToken.expire_at > current_time(), 
            models.RefreshToken.is_revoked == False,
        )
    )
    current_token = current_token.scalar_one_or_none()
    
    if current_token is None:
        raise ValueError("Refresh token not found, expired, or already revoked")
    
    current_token.is_revoked = True
    db_session.commit()
    
    new_raw_token = create_refresh_token(
        user_id = current_token.user_id,
        device_name = current_token.device_name,
        ip_address = current_token.ip_address,
        db_session = db_session,
    )
    
    return new_raw_token

    
def revoke_refresh_token(raw_token: str, db_session) -> None:
    
    token_hash: str = hash_string(raw_token)
    
    current_token = db_session.execute(
        select(models.RefreshToken).where(
            models.RefreshToken.token_hash == token_hash, 
            models.RefreshToken.is_revoked == False,
        )
    )
    current_token = current_token.scalar_one_or_none()
    
    if current_token is None:
        raise ValueError("Refresh token not found or already revoked")
    
    current_token.is_revoked = True
    db_session.commit()


def revoke_all_refresh_tokens(user_id: int, db_session) -> None:

    try:
        db_session.execute(
            update(models.RefreshToken).where(
                models.RefreshToken.user_id == user_id,
                models.RefreshToken.is_revoked == False,
            ).values(is_revoked = True)
        )
        
        db_session.commit()
    except Exception as e:
        log_error("revoke_all_refresh_tokens", e)


def create_access_token(user_id: int) -> str:
    
    payload = {
        "sub": str(user_id),
        "iat": current_time(),
        "exp": current_time() + ACCESS_LIFESPAN,
    }
    
    return jwt.encode(
        payload, 
        SECRET_KEY, 
        algorithm= ALGORITHM,
    )


def on_password_change(user_id: int, raw_token: str, db_session):
    
    token_hash: str = hash_string(raw_token)
    
    current_token = db_session.execute(
        select(models.RefreshToken).where(
            models.RefreshToken.token_hash == token_hash,
            models.RefreshToken.expire_at > current_time(), 
            models.RefreshToken.is_revoked == False,
        )
    )
    current_token = current_token.scalar_one_or_none()
    
    if current_token is None:
        raise ValueError("Refresh token not found, expired, or already revoked")
    
    user_ip_address = current_token.ip_address
    user_device_name = current_token.device_name
    
    revoke_all_refresh_tokens(user_id, db_session)
    
    new_raw_refresh = create_refresh_token(
        user_id = user_id,
        device_name = user_device_name,
        ip_address = user_ip_address,
        db_session = db_session,
    )
    
    return {
        "access_token" : create_access_token(user_id),
        "refresh_token" : new_raw_refresh,
    }
