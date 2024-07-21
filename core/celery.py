from celery import Celery
from celery.result import AsyncResult
from core.config import settings

RABBITMQ_USER = settings.RABBITMQ_USER
RABBITMQ_URL = settings.RABBITMQ_URL
RABBITMQ_VHOST = settings.RABBITMQ_VHOST
RABBITMQ_PASS = settings.RABBITMQ_PASS

celery_app = Celery(
    "TestQ",
    broker=f"pyamqp://{RABBITMQ_USER}:{RABBITMQ_PASS}@{RABBITMQ_URL}/{RABBITMQ_VHOST}", 
    backend="rpc://", 
    include=["utils.image_processing"]
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

def get_task_info(task_id):
    """
    return task info for the given task_id
    """
    task_result = AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }
    return result
