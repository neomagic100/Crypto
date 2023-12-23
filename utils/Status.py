from dateutil import parser

class Status():
    def __init__(self, status):
        self.timestamp = parser.parse(status["timestamp"])
        self.error_code = int(status["error_code"])
        self.error_message = status["error_message"]
        self.elapsed = int(status["elapsed"])
        self.credit_count = int(status["credit_count"])
        self.notice = status["notice"]
        self.total_count = int(status["total_count"])
