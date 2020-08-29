from analysis.analysis import Analysis
from monitoring.new_monitoring import EASEMonitoring
import re


class EASEAnalysis(Analysis):

    def __init__(self, mongodb_client, monitoring :EASEMonitoring):
        super().__init__(mongodb_client)
        self.monitoring = monitoring
        self.arrival_rate = None
        self.response_time = None
        self.data_payload = None

    def get_property(self, pattern, text):
        # returns first group of that property
        m = re.search(pattern, text)
        if m is None:
            raise Exception("CANNOT FIND REQUESTS PER SECOND")
        else:
            return float(m.group(2))

    def update(self):
        raw_results = self.monitoring.raw_results
        # arrival rate
        self.arrival_rate = self.get_property(r"(Requests per second:    )([\d.]*)( \[)", raw_results)

        # response time
        self.response_time = self.get_property(r"(Time per request:       )([\d.]*)( \[)", raw_results)
        # data payload
        self.data_payload = self.get_property(r"(Document Length:        )([\d.]*)( bytes)", raw_results)
        data = {
            "arrival_rate(req/s)": self.arrival_rate,
            "response_time(ms)": self.response_time,
            "data payload(bytes)": self.data_payload
        }
        print("MEASUREMENTS:", data)
        super().notify()
