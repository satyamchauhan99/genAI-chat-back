from celery import Celery

# Create Celery app instance
celery_app = Celery(
    "worker",
    broker="redis://localhost:6379/0",     
    backend="redis://localhost:6379/0",   
)

# Optional configurations
celery_app.conf.update(
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    timezone='UTC',
    enable_utc=True,
)

# Task routes
celery_app.conf.task_routes = {
    "tasks.digest_document": {"queue": "digest"},
}