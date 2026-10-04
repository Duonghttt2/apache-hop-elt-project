from flask import Flask, jsonify
import subprocess

app = Flask(__name__)

# tạo 1 endpoint(url) để kích hoạt etl
@app.route('/api/trigger-etl', methods=['GET', 'POST'])
def trigger_etl():
    try:
        # đường dẫn tới file chạy tự động
        bat_file_path = r"D:\apache-hop-project\Scheduling\etl_auto.bat"
        # gọi hệ thống chạy file bat ngầm
        subprocess.Popen(bat_file_path, shell=True)

        # trả về kết quả response báo thành công
        return jsonify({
            'status': 'success',
            'message': 'ETL process triggered successfully',
            "workflow": "03_data_workflow.hwf"
        })
    except Exception as e:
        # báo lỗi hệ thống ko gọi dc file
        return jsonify({
            "status": "error",
            "message": "Failed to trigger ETL process"
        })
if __name__ == '__main__':
    # chạy server ở cổng 5000
    app.run(host='0.0.0.0', port=5000)
