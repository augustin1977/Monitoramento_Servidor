from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from users import get_user_by_token

security = HTTPBearer(auto_error=False)  # Não bloqueia automaticamente

def validate_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if not credentials:
        raise HTTPException(status_code=401, detail="Token não enviado")

    token = credentials.credentials
    user = get_user_by_token(token)
    if not user:
        raise HTTPException(status_code=403, detail="Token inválido")

    return user  # retorna o usuário associado ao token
