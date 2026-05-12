from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import redis
from config import Config
from app.models import get_db_connection

app = Flask(__name__)
CORS(app)

r = redis.Redis(host=Config.REDIS_HOST, port=Config.REDIS_PORT, db=Config.REDIS_DB)

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/current')
def current_metrics():
    data = r.hgetall("current_metrics")
    if not data:
        return jsonify({"error": "No data"}), 404
    result = {k.decode(): v.decode() for k, v in data.items()}
    for k in ['cpu_percent', 'mem_percent', 'disk_percent']:
        if k in result:
            result[k] = float(result[k])
    return jsonify(result)

@app.route('/api/history')
def history_metrics():
    hours = request.args.get('hours', default=24, type=int)
    host_id = 1
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("""
            SELECT metric_time, cpu_percent, mem_percent, disk_percent
            FROM metrics_history
            WHERE host_id = %s AND metric_time > DATE_SUB(NOW(), INTERVAL %s HOUR)
            ORDER BY metric_time ASC
        """, (host_id, hours))
        rows = cur.fetchall()
    conn.close()
    for row in rows:
        row['metric_time'] = row['metric_time'].isoformat()
    return jsonify(rows)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)