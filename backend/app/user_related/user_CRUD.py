from backend.database import models
from backend.timestamps import current_time
from backend.logging import log_info, current_function
from backend.private_logic.hashing import algorithm, hash_salt
from backend.security.jwt_tokens import create_jwt

def new_user_register(username: str, email: str, password: str, db_session, policy_agreement: bool = False, role: int = 1) -> bool:
    '''
    Makes query and performs INSERT operation to add user to the database.
    It takes username, email, password, policy_agreement, role, db_session and returns bool value to determine weather operation was a success or not.
    '''
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
        models.user_login_credentials.id_user,
        models.user_login_credentials.email,
        models.user_login_credentials.hashed_password,
    ).filter(
        models.user_login_credentials.email == email,
    ).first()
    if correct_credentials is not None and correct_credentials.email == email and correct_credentials.hashed_password == hashed_password:
        login_data: bool =  True
    else:
        login_data: bool =  False

    #!----TO BE REDIRECTED TO user_session.py----
    if login_data:
    #----Create JWT----
        access_token, payload = create_jwt(correct_credentials.id_user, issue_endpoint='/login_request', for_endpoint='/loged')
    #----Add User Session Entry----
        login_session = models.login_session(
            user_id = correct_credentials.id_user,
            access_token = access_token,
            issued_at = payload['iat'],
            valid_till = payload['exp'],
            issued_from_endpoint = '/user_request',
            valid_for_endpoint = payload['aud'],
            status = 'Active',
            jwt_id = payload['jti'],
            created_at = str(current_time()),
        )
        try:
            db_session.add(login_session)
            db_session.commit()
        except Exception as e:
            db_session.rollback()
            log_info(current_function, e)
        return True, access_token
    else:
        return False, None
    
def user_log_out(db_session, access_token: str = None):
    ''' '''

    status: list[any] = db_session.query(
        models.login_session.status,
        models.login_session.valid_till,
    ).filter(
        models.login_session.access_token == access_token,
    ).order_by(
        models.login_session.issued_at.desc()
    ).first()
    if status is None:
        log_info(current_function, 'Status is None', f'Parameters passed: access_token "{access_token}"')
    elif type(status) != str:
        log_info(current_function, f'Incorrect status: {status}')
        raise Exception
    else:
        log_info(current_function, f'Status is {status[0]}')

        if status[0] == 'Active':
            try:
                db_session.query(
                models.login_session,
                ).filter_by(
                    access_token = access_token,
                ).update(
                    {'status': 'Revoked'}
                )
                db_session.commit()
            except Exception as e:
                db_session.rollback()
                log_info('Log Out', e)
                return False
            return True
        elif status[0] == 'Revoked':
            log_info(current_function, 'Token is already revoked')
            return False
        else:
            log_info(current_function, 'Unexpected Value')
            return False