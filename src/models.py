# Class ServiceRequest (bước 4)
"""models.py - Class đại diện cho một bản ghi yêu cầu dịch vụ 311."""


class ServiceRequest:
    """Một dòng trong file CSV, sau khi đã được làm sạch."""

    def __init__(self, unique_key, created, closed,
                 agency, complaint_type, status, borough):
        self.unique_key = unique_key          # chuỗi, ví dụ "60000001"
        self.created = created                # datetime hoặc None
        self.closed = closed                  # datetime hoặc None
        self.agency = agency                  # ví dụ "NYPD"
        self.complaint_type = complaint_type  # ví dụ "Noise - Residential"
        self.status = status                  # "Closed", "Open"... hoặc "" nếu thiếu
        self.borough = borough                # ví dụ "BROOKLYN"

    @property
    def closure_hours(self):
        """Số giờ từ lúc tạo đến lúc đóng.

        Trả về None nếu không tính được: thiếu một trong hai mốc thời gian,
        hoặc ngày đóng sớm hơn ngày tạo (dữ liệu chưa đúng).
        """
        if self.created is None or self.closed is None:
            return None
        seconds = (self.closed - self.created).total_seconds()
        if seconds < 0:
            return None
        return seconds / 3600

    def __repr__(self):
        return (f"ServiceRequest({self.unique_key}, {self.agency}, "
                f"{self.complaint_type}, {self.status})")