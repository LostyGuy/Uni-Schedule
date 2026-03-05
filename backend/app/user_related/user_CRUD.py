from backend.database import models
from backend.timestamps import current_time
from backend.logging import log_info, current_function
from backend.private_logic.hashing import algorithm, hash_salt # type: ignore
from backend.security.jwt_tokens import create_jwt

def new_user_register(email: str, password:str, policy_agreement: bool, role:int, db_session, algorithm) -> None:
    try:
        new_user = models.user_login_credentials(
            email = email,
            hashed_password = hash_password(password, algorithm=algorithm),
            created_at = current_time(),
            policy_agreement = policy_agreement,
            lastly_signed_in_on = current_time(),
            role = role,
        )
        db_session.add(new_user)
    except Exception as e:
        log_info(current_function, e)
    finally:
        db_session.commit()

def hash_password(password, algorithm, hash_salt) -> str:
    return algorithm((password + hash_salt).encode()).hexdigest()

def is_user_in_database(email, db_session) -> int:
    raise NotImplementedError

def user_login(email:str, hashed_password:str, db_session) -> list[str,str,str,str]:
    
    #----If User In Database----
    user_id = is_user_in_database(email)
    if user_id:
    #----Create JWT----
        access_token = create_jwt(user_id)
    #----Add User Session Entry----
    
    #----Set Cookie----
        return access_token