# HƯỚNG DẪN SỬ DỤNG HỆ THỐNG TỰ ĐỘNG HÓA ETL

## Apache Hop + Python Flask API + Scheduler + PostgreSQL

---

## 1. Mục đích của hệ thống

Hệ thống được xây dựng để tự động hóa quy trình ETL:

**Excel đầu vào → Apache Hop xử lý → Staging → PostgreSQL Data Warehouse → Output/Log**

Ngoài việc chạy pipeline ETL, hệ thống còn có Python Flask API để kích hoạt quá trình xử lý theo yêu cầu và Scheduler để chạy tự động theo lịch.

---

# 2. Cấu trúc thư mục

Sau khi tải project về, cấu trúc thư mục dự kiến:

```text
apache-hop-project/
│
├── Code/
│   ├── api_trigger.py
│   ├── scheduler.py
│   └── requirements.txt
│
├── Config/
│   └── .env.example
│
├── Input/
│   └── [các file Excel đầu vào]
│
├── Output/
│   ├── [dữ liệu chuẩn]
│   └── [dữ liệu lỗi]
│
├── Log/
│   └── [file log]
│
├── Pipelines/
│   └── *.hpl
│
├── Workflows/
│   └── *.hwf
│
└── Scheduling/
    ├── *.bat
    └── *.sh
```

### Chức năng từng thư mục

| Thư mục       | Chức năng                              |
| ------------- | -------------------------------------- |
| `Code/`       | Mã Python cho API và Scheduler         |
| `Config/`     | Cấu hình hệ thống, biến môi trường     |
| `Input/`      | Nơi đưa file Excel vào để ETL xử lý    |
| `Output/`     | Kết quả sau xử lý và dữ liệu lỗi       |
| `Log/`        | Lưu nhật ký chạy ETL                   |
| `Pipelines/`  | Các pipeline Apache Hop (`.hpl`)       |
| `Workflows/`  | Các workflow Apache Hop (`.hwf`)       |
| `Scheduling/` | Script chạy tự động trên Windows/Linux |

---

# 3. Yêu cầu trước khi chạy

Cần chuẩn bị:

- Windows, Linux hoặc macOS
- Python 3.x
- Apache Hop
- PostgreSQL
- Git
- Quyền truy cập vào database PostgreSQL
- Các pipeline/workflow của project

Kiểm tra Python:

```bash
python --version
```

Kiểm tra Git:

```bash
git --version
```

Kiểm tra Apache Hop bằng cách mở ứng dụng Apache Hop.

---

# 4. Tải project

Mở **CMD / PowerShell / Terminal**.

Chuyển tới thư mục muốn lưu project, sau đó chạy:

```bash
git clone <địa_chỉ_repo_github_của_dự_án>
```

Sau khi tải xong:

```bash
cd apache-hop-project
```

Kiểm tra project:

```bash
dir
```

Trên Linux/macOS có thể dùng:

```bash
ls
```

Phải thấy các thư mục chính như:

```text
Code
Config
Input
Output
Log
Pipelines
Workflows
Scheduling
```

---

# 5. Cài thư viện Python

Trong thư mục gốc của project chạy:

```bash
pip install -r Code/requirements.txt
```

Hoặc:

```bash
python -m pip install -r Code/requirements.txt
```

Kiểm tra Flask:

```bash
python -c "import flask; print('Flask OK')"
```

Kiểm tra APScheduler:

```bash
python -c "import apscheduler; print('APScheduler OK')"
```

---

# 6. Tạo file cấu hình `.env`

Trong thư mục `Config/`, tìm file:

```text
.env.example
```

Tạo một bản sao và đổi tên thành:

```text
.env
```

Ví dụ:

```text
Config/
├── .env.example
└── .env
```

Mở file `.env` và điền thông tin PostgreSQL thực tế:

```env
DB_HOST=127.0.0.1
DB_PORT=5432
DB_USER=postgres
DB_PASS=mat_khau_database
```

Nếu `.env.example` có thêm biến khác thì phải điền đầy đủ theo project.

## Lưu ý bảo mật

Không đưa mật khẩu thật vào GitHub.

Nên thêm vào `.gitignore`:

```gitignore
.env
```

---

# 7. Cấu hình PostgreSQL

Chuẩn bị database mà Apache Hop sẽ sử dụng.

Các thông tin cần biết:

```text
Host     = 127.0.0.1
Port     = 5432
Database = [tên database]
User     = [tên đăng nhập]
Password = [mật khẩu]
```

Đảm bảo PostgreSQL đang chạy trước khi thực hiện ETL.

---

# 8. Cấu hình Apache Hop

Mở **Apache Hop**.

Vào:

**Projects / Project Manager → Add a new project**

Chọn project vừa tải về.

Home folder trỏ tới thư mục:

```text
apache-hop-project
```

Ví dụ:

```text
D:\DuAn\apache-hop-project
```

Sau đó lưu project.

---

# 9. Cấu hình biến môi trường trong Apache Hop

Trong Apache Hop mở **Environment Configuration**.

Khai báo các biến tương ứng với project:

```text
DB_HOST = 127.0.0.1
DB_PORT = 5432
DB_USER = postgres
DB_PASS = mật_khẩu_database
```

Các giá trị phải khớp với cấu hình database mà project sử dụng.

---

# 10. Kiểm tra pipeline và workflow

## Pipeline

Trong thư mục:

```text
Pipelines/
```

Các file có dạng:

```text
*.hpl
```

Pipeline thực hiện các bước ETL như:

```text
Input Excel
    ↓
Đọc dữ liệu
    ↓
Làm sạch
    ↓
Chuẩn hóa
    ↓
Staging
    ↓
Data Warehouse
```

## Workflow

Trong thư mục:

```text
Workflows/
```

Các file có dạng:

```text
*.hwf
```

Workflow dùng để điều phối pipeline và các bước xử lý theo đúng thứ tự.

---

# 11. Chuẩn bị dữ liệu đầu vào

Đưa file Excel cần xử lý vào:

```text
Input/
```

Ví dụ:

```text
Input/
├── phim_01.xlsx
├── phim_02.xlsx
└── phim_03.xlsx
```

Trước khi chạy nên kiểm tra:

- File đúng định dạng Excel.
- Tên file đúng quy ước của project.
- Các cột đúng cấu trúc mà pipeline yêu cầu.
- File không bị khóa/đang mở bằng Excel.
- Dữ liệu đủ trường bắt buộc.

---

# 12. Chạy hệ thống bằng Python API

Mở Terminal/CMD tại thư mục gốc:

```text
apache-hop-project
```

Chạy:

```bash
python Code/api_trigger.py
```

Nếu thành công, Flask server sẽ khởi động theo cấu hình của project.

Terminal thường hiển thị thông tin server, ví dụ:

```text
Running on http://127.0.0.1:5000
```

**Không tự thay đổi port nếu project đã quy định port riêng.**

---

# 13. Kích hoạt ETL qua API

`api_trigger.py` có nhiệm vụ cung cấp API để gọi quá trình ETL.

Endpoint cụ thể phải được lấy từ code thực tế của:

```text
Code/api_trigger.py
```

Cần kiểm tra:

- API chạy tại port nào.
- Endpoint là gì.
- Phương thức request là `GET` hay `POST`.
- Có cần truyền tham số không.
- API gọi pipeline/workflow nào.

Ví dụ nếu code có:

```python
@app.route("/run-etl", methods=["POST"])
```

thì endpoint là:

```text
http://127.0.0.1:5000/run-etl
```

Có thể dùng Postman, PowerShell, curl hoặc ứng dụng khác để gửi request.

### Quan trọng

Không sử dụng `/run-etl` như endpoint chính thức nếu `api_trigger.py` không khai báo endpoint này. Phải lấy đúng endpoint từ source code của project.

---

# 14. Chạy Scheduler tự động

Nếu project có:

```text
Code/scheduler.py
```

thì Scheduler có nhiệm vụ tự động kích hoạt ETL theo lịch.

Chạy:

```bash
python Code/scheduler.py
```

Hoặc dùng script trong:

```text
Scheduling/
```

Windows thường sử dụng:

```text
*.bat
```

Linux/macOS thường sử dụng:

```text
*.sh
```

---

# 15. Luồng hoạt động tổng quát

```text
1. Đưa Excel vào Input/
          ↓
2. Python API / Scheduler kích hoạt ETL
          ↓
3. Apache Hop chạy Workflow
          ↓
4. Workflow gọi Pipeline
          ↓
5. Pipeline đọc Excel
          ↓
6. Làm sạch dữ liệu
          ↓
7. Chuẩn hóa dữ liệu
          ↓
8. Đưa dữ liệu vào Staging
          ↓
9. Nạp dữ liệu vào PostgreSQL Data Warehouse
          ↓
10. Xuất dữ liệu chuẩn / dữ liệu lỗi
          ↓
11. Ghi Log
```

---

# 16. Kiểm tra kết quả sau khi chạy

## 16.1. Kiểm tra Output

Mở:

```text
Output/
```

Kiểm tra các file dữ liệu chuẩn và dữ liệu lỗi theo thiết kế project.

## 16.2. Kiểm tra Log

Mở:

```text
Log/
```

Kiểm tra:

- Pipeline có chạy không.
- Workflow có chạy không.
- Có lỗi đọc Excel không.
- Có lỗi kết nối PostgreSQL không.
- Có lỗi xử lý dữ liệu không.
- Số lượng bản ghi thành công/thất bại nếu log có ghi nhận.

## 16.3. Kiểm tra Staging

Trong PostgreSQL kiểm tra bảng Staging:

- Có dữ liệu mới không.
- Số dòng có hợp lý không.
- Kiểu dữ liệu có đúng không.
- Dữ liệu đã được chuẩn hóa chưa.

## 16.4. Kiểm tra Data Warehouse

Ví dụ:

```sql
SELECT COUNT(*)
FROM ten_bang;
```

Xem dữ liệu:

```sql
SELECT *
FROM ten_bang
LIMIT 20;
```

Tên bảng thực tế phải lấy theo database của project.

---

# 17. Khi chạy lại ETL

Cần xác định project đang dùng cách nào:

### Append

Dữ liệu mới được thêm vào dữ liệu cũ:

```text
Dữ liệu cũ + dữ liệu mới
```

### Replace

Xóa dữ liệu cũ rồi nạp lại:

```text
Xóa dữ liệu cũ
      ↓
Nạp dữ liệu mới
```

### Upsert

Có bản ghi thì cập nhật, chưa có thì thêm mới:

```text
Có rồi → UPDATE
Chưa có → INSERT
```

Phải kiểm tra logic pipeline/workflow trước khi chạy lại để tránh:

- Trùng dữ liệu.
- Chèn dữ liệu nhiều lần.
- Lỗi khóa chính.
- Lỗi unique constraint.

---

# 18. Xử lý lỗi cơ bản

## Không tìm thấy Python

```bash
python --version
```

Kiểm tra lại Python và PATH.

## Thiếu thư viện Flask/APScheduler

```bash
pip install -r Code/requirements.txt
```

## Không kết nối PostgreSQL

Kiểm tra:

```text
DB_HOST
DB_PORT
DB_USER
DB_PASS
```

và kiểm tra PostgreSQL đang chạy.

## Apache Hop không đọc được project

Kiểm tra:

- Home folder đúng thư mục project.
- Project có `Pipelines/` và `Workflows/`.
- Đường dẫn file đúng.
- Biến môi trường đã khai báo.

## Pipeline chạy nhưng không có dữ liệu

Kiểm tra theo chuỗi:

```text
Input/
  ↓
Pipeline Input
  ↓
Transform / Filter
  ↓
Staging
  ↓
Data Warehouse
  ↓
Output/
```

Xác định dữ liệu dừng ở bước nào thay vì chỉ kiểm tra bảng cuối cùng.

---

---

# 21. Các lệnh thường dùng

### Tải project

```bash
git clone <địa_chỉ_repo>
```

### Vào project

```bash
cd apache-hop-project
```

### Cài thư viện

```bash
pip install -r Code/requirements.txt
```

### Chạy API

```bash
python Code/api_trigger.py
```

### Chạy Scheduler

```bash
python Code/scheduler.py
```

---
