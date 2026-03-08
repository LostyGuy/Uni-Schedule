import jwt
from backend.private_logic.jwt import SECRET_KEY, ALGORITHM, TOKEN_LIFESPAN
from backend.timestamps import current_time
from backend.logging import current_function, log_info
import uuid


def create_jwt(user_id: int, issue_endpoint: str, for_endpoint: str) -> str:
    payload = {
        'iss' : 'uni-schedule/api' ,
        'sub' : int(user_id),
        'aud' : '/loged' ,
        'exp' : str(current_time()) ,
        'iat' : str(current_time() + TOKEN_LIFESPAN) ,
        'jti' : str(uuid.uuid4()) ,
    }
    access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return access_token, payload
    
def jwt_validation(sth) -> bool:
    raise NotImplementedError

# iss (issuer): Issuer of the JWT
# sub (subject): Subject of the JWT (the user)
# aud (audience): Recipient for which the JWT is intended
# exp (expiration time): Time after which the JWT expires
# iat (issued at time): Time at which the JWT was issued; can be used to determine age of the JWT
# jti (JWT ID): Unique identifier; can be used to prevent the JWT from being replayed (allows a token to be used only once)