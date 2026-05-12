import pymysql
import redis
from config import Config

def get_db_connection():
    return pymysql.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DB,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

def get_host_id(hostname='ubuntu-local'):
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT id FROM hosts WHERE hostname = %s", (hostname,))
        row = cur.fetchone()
        if row:
            return row['id']
        else:
            cur.execute("INSERT INTO hosts (hostname) VALUES (%s)", (hostname,))
            conn.commit()
            return cur.lastrowid
    conn.close()

def insert_metrics(host_id, metrics):
    conn = get_db_connection()
    with conn.cursor() as cur:
        sql = """
            INSERT INTO metrics_history 
            (host_id, metric_time, cpu_percent, mem_total, mem_used, mem_percent,
             disk_total, disk_used, disk_percent, net_sent, net_recv)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cur.execute(sql, (
            host_id, metrics['metric_time'], metrics['cpu_percent'],
            metrics['mem_total'], metrics['mem_used'], metrics['mem_percent'],
            metrics['disk_total'], metrics['disk_used'], metrics['disk_percent'],
            metrics['net_sent'], metrics['net_recv']
        ))
        conn.commit()
    conn.close()

def save_current_to_redis(metrics):
    r = redis.Redis(host=Config.REDIS_HOST, port=Config.REDIS_PORT, db=Config.REDIS_DB)
    r.hset("current_metrics", mapping={
        'cpu_percent': metrics['cpu_percent'],
        'mem_percent': metrics['mem_percent'],
        'disk_percent': metrics['disk_percent'],
        'net_sent': metrics['net_sent'],
        'net_recv': metrics['net_recv'],
        'update_time': metrics['metric_time'].isoformat()
    })
    r.expire("current_metrics", 7200)