from pydantic import BaseModel


class UserServiceConfig(BaseModel):
    app_name: str = "ates-user-service"
    environment: str = "local"
    log_level: str = "DEBUG"
    shared_secret: str = "ates-shared-secret"
    jwt_ttl: int = 86400
    db_connstring: str = "postgresql://postgres:postgres@localhost:5432/user_service"


config = UserServiceConfig()
