from datetime import datetime

from pymongo import MongoClient

from src.config import Settings


class MongoDBRepository(object):
    def __init__(self, settings: Settings):
        self._client = MongoClient(f"mongodb://{settings.MONGODB_HOST}:{settings.MONGODB_PORT}")
        self._my_collection = self._client[settings.MONGODB_NAME][settings.MONGODB_COLLECTION_NAME]

    def get_data_using_algorithm(
            self,
            dt_upto: str,
            group_type: str,
            dates: list,
    ):
        dt_upto: datetime = datetime.strptime(dt_upto, "%Y-%m-%dT%H:%M:%S")
        data: dict = {"dataset": [], "labels": []}

        for cur_date in dates[1:]:
            summary: int = 0

            prev_date = dates[dates.index(cur_date) - 1]

            predicate = "$lte" if cur_date == dates[-1] else "$lt"

            for document in self._my_collection.find({"dt": {"$gte": prev_date, f"{predicate}": cur_date}}):
                if group_type == "hour" and (dt_upto.hour == 0 and dt_upto.minute == 0) and cur_date == dates[-1]:
                    # не суммирую зарплаты, если dt_upto равна <дата>T00:00:00, так как мне не нужен следующий час
                    summary += 0
                elif group_type == "day" and (dt_upto.hour == 0 and dt_upto.minute == 0) and cur_date == dates[-1]:
                    # не суммирую зарплаты, если dt_upto равна <дата>T00:00:00, так как мне не нужен следующий день
                    summary += 0
                else:
                    summary += document.get("value")

            data["dataset"].append(summary)
            data["labels"].append(prev_date.isoformat())

        return data
