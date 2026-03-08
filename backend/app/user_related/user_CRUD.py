from backend.database import models
from backend.timestamps import current_time
from backend.logging import log_info, current_function
from backend.private_logic.hashing import algorithm, hash_salt
from backend.security.jwt_tokens import create_jwt
from

def new_user_register(username:str, email: str, password:str, policy_agreement: bool, role:int, db_session) -> bool:
    if policy_agreement:
        try:
            new_user = models.user_login_credentials(
                username = username,
                email = email,
                hashed_password = hash_password(password, hash_salt),
                created_at = current_time(),
                policy_agreement = policy_agreement,
                lastly_signed_in_on = current_time(),
                role = role,
            )
            db_session.add(new_user)
            db_session.commit()
            return True
        except Exception as e:
            db_session.rollback()
            log_info(current_function, e)
            return False
    else:
        return False

def hash_password(password, hash_salt) -> str:
    return algorithm((password + hash_salt).encode()).hexdigest()

def user_login(email:str, hashed_password:str, db_session) -> bool:
    
    #----Is Credentials Correct----
    correct_credentials: list[object] = db_session.query(
        models.user_login_credentials.id,
        models.user_login_credentials.email,
        models.user_login_credentials.hashed_password,
    ).filter(
        models.user_login_credentials.email == email,
    ).first()
    if correct_credentials is not None and correct_credentials.email == email and correct_credentials.hashed_password == hashed_password:
        login_data: bool =  True
    else:
        login_data: bool =  False

    if login_data:
    #----Create JWT----
        access_token, payload = create_jwt(correct_credentials.id, issue_endpoint='/login_request', for_endpoint='/loged')
    #----Add User Session Entry----
        login_session = models.login_session(
            user_id = correct_credentials.id,
            access_token = access_token,
            issued_at = payload['iat'],
            valid_till = payload['exp'],
            issued_from_endpoint = '/user_request',
            valid_for_endpoint = payload['aud'],
            status = 'active',
            jwt_id = payload['jti'],
            created_at = str(current_time()),
        )
        try:
            db_session.add(login_session)
            db_session.commit()
        except Exception as e:
            db_session.rollback()
            log_info(current_function, e)
        return True
    else:
        return False