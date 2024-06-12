from pymongo import MongoClient

from src.config import Settings


class MongoDBRepository(object):
    def __init__(self, settings: Settings):
        self._client = MongoClient(f"mongodb://{settings.MONGODB_HOST}:{settings.MONGODB_PORT}")
        self._my_collection = self._client[settings.MONGODB_NAME][settings.MONGODB_COLLECTION_NAME]

    def get_data_using_algorithm(
            self,
            group_type: str,
            dates: list,
    ):
        data: dict = {"dataset": [], "labels": []}

        for cur_date in dates[1:]:
            summary: int = 0

            prev_date = dates[dates.index(cur_date) - 1]

            predicate = "$lte" if cur_date == dates[-1] else "$lt"

            for document in self._my_collection.find({"dt": {"$gte": prev_date, f"{predicate}": cur_date}}):
                summary += 0 if group_type == "hour" and cur_date == dates[-1] else document.get("value")

            data["dataset"].append(summary)
            data["labels"].append(prev_date.isoformat())

        return data
