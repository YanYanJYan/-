from app.models import get_db_connection, get_host_id
import datetime

def check_and_alert(metric_name, current_value):
    """检查是否触发告警，返回是否触发"""
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT threshold FROM alert_rules WHERE metric_name=%s AND enabled=1", (metric_name,))
        rule = cur.fetchone()
        if not rule:
            return False
        threshold = rule['threshold']
        if current_value >= threshold:
            host_id = get_host_id()
            # 检查最近5分钟是否已有该告警
            cur.execute("""
                SELECT id FROM alert_events 
                WHERE host_id=%s AND metric_name=%s AND resolved=0 
                AND alert_time > %s
            """, (host_id, metric_name, datetime.datetime.now() - datetime.timedelta(minutes=5)))
            if cur.fetchone():
                conn.close()
                return False
            # 记录告警
            message = f"{metric_name} = {current_value:.2f} (阈值 {threshold})"
            cur.execute("""
                INSERT INTO alert_events (host_id, metric_name, trigger_value, message, alert_time)
                VALUES (%s, %s, %s, %s, %s)
            """, (host_id, metric_name, current_value, message, datetime.datetime.now()))
            conn.commit()
            # 简单打印告警
            print(f"[ALERT] {message}")
            conn.close()
            return True
    conn.close()
    return False