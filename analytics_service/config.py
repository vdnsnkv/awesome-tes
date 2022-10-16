from pydantic import BaseModel


class AnalyticsServiceConfig(BaseModel):
    app_name: str = "ates-analytics-service"
    environment: str = "local"
    log_level: str = "DEBUG"
    shared_secret: str = "ates-shared-secret"
    jwt_ttl: int = 86400
    db_connstring: str = (
        "postgresql://postgres:postgres@localhost:5432/analytics_service"
    )


config = AnalyticsServiceConfig()
