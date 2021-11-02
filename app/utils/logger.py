import os
import csv
from typing import Any


class Logger:
    def __init__(self, log_path: str, delimiter: str = ',') -> None:
        self._log_path = log_path
        self._header = not os.path.exists(log_path)
        self._delimiter = delimiter

    def log_object(self, object: dict[str, Any]) -> None:
        with open(self._log_path, 'a', newline='') as f_hand:
            sorted_obj = dict(sorted(object.items()))
            attrs = sorted_obj.keys()
            writer = csv.DictWriter(f_hand, attrs, delimiter=self._delimiter)
            if self._header: writer.writeheader()
            writer.writerow(sorted_obj)
