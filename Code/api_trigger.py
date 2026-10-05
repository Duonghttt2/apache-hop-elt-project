import os
import subprocess
from flask import Flask, jsonify
from apscheduler.schedulers.background import BackgroundScheduler # type: ignore

app = Flask(__name__)

# tạo 1 endpoint(url) để kích hoạt etl
@app.route('/api/trigger-etl', methods=['GET', 'POST'])
def trigger_etl():
    try:
        # Tự động định vị đường dẫn tới file chạy tự động (.bat)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        bat_file_path = os.path.join(os.path.dirname(current_dir), 'Scheduling', 'etl_auto.bat')

        # gọi hệ thống chạy file bat ngầm
        subprocess.Popen(bat_file_path, shell=True)
        
        # trả về kết quả response báo thành công
        return jsonify({
            'status': 'success',
            'message': 'ETL process triggered successfully',
            'workflow': "03_data_workflow.hwf"
        })
    except Exception as e:
        # báo lỗi hệ thống ko gọi dc file
        return jsonify({
            "status": "error",
            "message": "Failed to trigger ETL process",
            "details": str(e)
        })

def scheduled_job():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    bat_file_path = os.path.join(os.path.dirname(current_dir), 'Scheduling', 'etl_auto.bat')
    subprocess.Popen(bat_file_path, shell=True)

scheduler = BackgroundScheduler()
scheduler.add_job(func=scheduled_job, trigger="interval", minutes=60) # Chạy định kỳ 60 phút
scheduler.start()

if __name__ == '__main__':
    # chạy server ở cổng 5000
    app.run(host='0.0.0.0', port=5000)