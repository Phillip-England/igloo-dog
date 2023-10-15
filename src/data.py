
import json
import os

def create_cem_json():
    file_path = "./data/cem.json"

    if not os.path.exists(file_path):
        data = {
            "current_month": {
                "osat": "99",
                "taste": "99",
                "ace": "99",
                "speed": "99",
                "cleanliness": "99",
                "accuracy": "99"
            },
            "three_month_rolling": {
                "osat": "99",
                "taste": "99",
                "ace": "99",
                "speed": "99",
                "cleanliness": "99",
                "accuracy": "99"
            },
            "year_to_date": {
                "osat": "99",
                "taste": "99",
                "ace": "99",
                "speed": "99",
                "cleanliness": "99",
                "accuracy": "99"
            }
        }

        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)




