import jwt
from backend.private_logic.jwt import SECRET_KEY, ALGORITHM, TOKEN_LIFESPAN
from backend.timestamps import current_time


def create_jwt(user_id: int, issue_endpoint: str, for_endpoint: str) -> str:
    payload = {
        'user_id': user_id,
        'issued_at':  current_time(),
        'valid_till': current_time() + TOKEN_LIFESPAN,
        'issued_from_endpoint': issue_endpoint ,
        'valid_for_endpoint': for_endpoint ,
    }
    access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return access_token
    
    
def jwt_validation():
    raise NotImplementedError