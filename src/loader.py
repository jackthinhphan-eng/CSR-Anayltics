# Đọc CSV, parse ngày (bước 4)
"""loader.py - Đọc file CSV 311, parse ngày giờ, ghi lại lỗi."""
import csv
import sys
from datetime import datetime

from models import ServiceRequest

# Định dạng ngày của portal NYC Open Data, ví dụ "09/01/2025 12:05:00 AM".
# Khi có file thật, hãy mở ra kiểm tra lại; nếu khác thì chỉ cần sửa dòng này.
DATE_FORMAT = "%m/%d/%Y %I:%M:%S %p"

COL_KEY = "Unique Key"
COL_CREATED = "Created Date"
COL_CLOSED = "Closed Date"
COL_AGENCY = "Agency"
COL_COMPLAINT = "Complaint Type"
COL_STATUS = "Status"
COL_BOROUGH = "Borough"


def parse_date(text):
    """Chuyển chuỗi thành datetime.
    - Chuỗi rỗng -> None (bình thường, ví dụ yêu cầu chưa đóng).
    - Chuỗi sai định dạng -> raise ValueError để nơi gọi ghi nhận lỗi.
    """
    text = text.strip()
    if text == "":
        return None
    return datetime.strptime(text, DATE_FORMAT)


def load_requests(path):
    """Đọc CSV, trả về (requests, issues).
    requests: list các ServiceRequest
    issues:   dict chứa các vấn đề phát hiện được khi đọc,
              dùng cho quality report ở bước 5.
    """
    requests = []
    issues = {"malformed_timestamps": []}  # mỗi phần tử: (dòng, ID, tên cột, giá trị)

    # utf-8-sig: tự bỏ ký tự BOM đầu file nếu file được lưu từ Excel
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        # Dòng 1 là tiêu đề nên dữ liệu bắt đầu từ dòng 2
        for line_no, row in enumerate(reader, start=2):
            key = row.get(COL_KEY, "").strip()

            dates = {}
            for col in (COL_CREATED, COL_CLOSED):
                raw = row.get(col, "")
                try:
                    dates[col] = parse_date(raw)
                except ValueError:
                    dates[col] = None  # giữ bản ghi, chỉ bỏ ngày bị lỗi
                    issues["malformed_timestamps"].append(
                        (line_no, key, col, raw)
                    )

            requests.append(ServiceRequest(
                unique_key=key,
                created=dates[COL_CREATED],
                closed=dates[COL_CLOSED],
                agency=row.get(COL_AGENCY, "").strip(),
                complaint_type=row.get(COL_COMPLAINT, "").strip(),
                status=row.get(COL_STATUS, "").strip(),
                borough=row.get(COL_BOROUGH, "").strip(),
            ))

    return requests, issues


if __name__ == "__main__":
    # Chạy thử:  python src/loader.py  [đường dẫn CSV]
    path = sys.argv[1] if len(sys.argv) > 1 else "data/sample.csv"
    requests, issues = load_requests(path)

    print(f"Đọc được {len(requests)} bản ghi")
    bad = issues["malformed_timestamps"]
    print(f"Timestamp lỗi: {len(bad)}")
    for line_no, key, col, raw in bad:
        print(f"  dòng {line_no} | ID {key} | {col} | {raw!r}")

    for r in requests[:3]:
        hours = r.closure_hours
        shown = f"{hours:.2f} giờ" if hours is not None else "không tính được"
        print(f"{r} -> {shown}")