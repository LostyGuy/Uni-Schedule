from backend.database import models
from backend.timestamps import current_time
from backend.logging import log_info
from backend.private_logic.hashing import algorithm, hash_salt



def new_user_register(email: str, password:str, policy_agreement: bool, role:int, db_session, algorithm):
    try:
        new_user = models.user_login_credentials(
            email = email,
            hashed_password = hash_password(password, algorithm=algorithm),
            created_at = current_time(),
            policy_agreement = policy_agreement,
            lastly_signed_in_on = current_time(), #TODO: Set to 0000:00:00 etc. by default
            role = role,
        )
        db_session.add(new_user)
    except Exception as e:
        log_info(e)
    finally:
        db_session.commit()

def hash_password(password, algorithm, hash_salt):
    return algorithm((password + hash_salt).encode()).hexdigest()