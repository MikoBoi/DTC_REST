import json
import os

class Metrics:
    def __init__(self, file_path="./app/infrastructure/metrics/metrics.json"):
        self.file_path = file_path
        self.data = self.load_metrics()

    def load_metrics(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as file:
                return json.load(file)
        return {}

    def save_metrics(self):
        with open(self.file_path, "w") as file:
            json.dump(self.data, file, indent=4)

    def increment_failure(self, category: str):
        if category not in self.data:
            self.data[category] = {"success": 0, "failure": 0, "total": 0}
        self.data[category]["failure"] += 1
        self.data[category]["total"] += 1
        self.save_metrics()

    def increment_success(self, category: str):
        if category not in self.data:
            self.data[category] = {"success": 0, "failure": 0, "total": 0}
        self.data[category]["success"] += 1
        self.data[category]["total"] += 1
        self.save_metrics()

    def get_metrics(self):
        return self.data