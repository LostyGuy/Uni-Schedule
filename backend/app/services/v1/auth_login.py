import os

import backend.connection.models as models
import backend.security.tokens as tokens
from backend.security.hashing import hash_string
from sqlalchemy import select, update


def user_login(email:str, password:str, device_name: str, ip_address: str, db_session) -> str:
    """
    Authenticates a user by email and hashed password, and creates a login session on successful verification.
    
    Returns:
    	(access_token, refresh_token) if the email and hashed_password match a user in the database, (None) otherwise
    """
    
    try:
        is_entry_present = db_session.query(
            models.User.user_id
        ).filter(
            models.User.email == email,
            models.User.hashed_password == hash_string(password)
        ).first()
    except Exception:
        #TODO:
        #---- Get most possible errors and show them to user in a friendly way ----#
        return {
            "access_token": None,
            "refresh_token": None,
        }
        
    if is_entry_present is not None:
        if is_entry_present[0]:
            raw_refresh_token = tokens.create_refresh_token(
                user_id = is_entry_present[0],
                device_name = device_name,
                ip_address = ip_address,
                db_session = db_session,
            )

            client_access_token = tokens.create_access_token(is_entry_present[0])
            
            return {
                "access_token": client_access_token,
                "refresh_token": raw_refresh_token,
            }

        return {
            "access_token": client_access_token,
            "refresh_token": raw_refresh_token,
        }
    
    else:
        
        return {
            "access_token": None,
            "refresh_token": None,
        }
    
    
def user_log_out(db_session, raw_token: str = None) -> bool:
    ''' '''

    if not raw_token:
        return False
    #----If token is in DB----
    stmt = select(
            models.RefreshToken
            ).where(
                models.RefreshToken.token_hash == hash_string(raw_token)
            )
        
    try:
        result = db_session.scalars(stmt).one_or_none()
        db_session.execute(
            update(
                models.RefreshToken,
            ).where(
                models.RefreshToken.user_session_id == result.user_session_id,
            ).values(
                is_revoked= True,
            )
        )
        db_session.commit()

    except Exception:
        #TODO
        ...
        return False
    return True
        













    #---- OLD LOGIC ----#
    # if access_token is None:
    #     log_info(current_function, 'access_token is None')
    #     raise ValueError
    
    # status: list[any] = db_session.query(
    #     models.login_session.status,
    #     models.login_session.valid_till,
    # ).filter(
    #     models.login_session.access_token == access_token,
    # ).order_by(
    #     models.login_session.issued_at.desc()
    # ).first()
    
    # log_info(current_function, f'Status is {status[0]}')

    # if status[0] == 'Active':
    #     try:
    #         db_session.query(
    #         models.login_session,
    #         ).filter_by(
    #             access_token = access_token,
    #         ).update(
    #             {'status': 'Revoked'}
    #         )
    #         db_session.commit()
    #     except Exception as e:
    #         db_session.rollback()
    #         log_info('Log Out', e)
    #         return False
    #     return True
    # elif status[0] == 'Revoked':
    #     log_info(current_function, 'Token is already revoked')
    #     return False
    # else:
    #     log_info(current_function, 'Unexpected Value')
    #     return False