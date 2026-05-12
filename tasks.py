from celery import Celery
from config import Config
from app.monitor import collect_metrics
from app.models import get_host_id, insert_metrics, save_current_to_redis
from app.alert import check_and_alert

celery_app = Celery('monitor_tasks', broker=Config.CELERY_BROKER_URL, backend=Config.CELERY_RESULT_BACKEND)
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Asia/Shanghai',
    enable_utc=True,
)

celery_app.conf.beat_schedule = {
    'collect-every-60s': {
        'task': 'app.tasks.collect_and_store',
        'schedule': 60.0,
    },
}


@celery_app.task
def collect_and_store():
    metrics = collect_metrics()
    host_id = get_host_id()
    insert_metrics(host_id, metrics)
    save_current_to_redis(metrics)

    check_and_alert('cpu_percent', metrics['cpu_percent'])
    check_and_alert('mem_percent', metrics['mem_percent'])
    check_and_alert('disk_percent', metrics['disk_percent'])

    return f"Collected at {metrics['metric_time']}"