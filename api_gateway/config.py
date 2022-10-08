from pydantic import BaseModel

APP_NAME = "ates-api-gateway"
SECRET = "secret"
API_PREFIX = "/api"
LOG_LEVEL = "DEBUG"
DB_CONNSTRING = "postgresql://postgres:postgres@localhost:5432"


class APIGatewayConfig(BaseModel):
    pass
