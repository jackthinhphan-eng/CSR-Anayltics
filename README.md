# NYC 311 Service Request Analytics

Phân tích dữ liệu NYC 311 và dựng dashboard offline bằng Python.

## Cài đặt

1. Tạo môi trường ảo: `python -m venv venv`
2. Kích hoạt môi trường ảo (xem hướng dẫn theo hệ điều hành)
3. Cài thư viện: `pip install -r requirements.txt`
4. Kiểm tra: `python src/check_env.py`

## Cấu trúc

- `data/`    : file CSV đã lọc từ NYC Open Data
- `src/`     : mã nguồn
- `outputs/` : báo cáo, file CSV kết quả, biểu đồ
- `DATA_SOURCE.md` : mô tả nguồn dữ liệu và bộ lọc đã dùng
