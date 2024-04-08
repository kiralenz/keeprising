import pandas as pd
from datetime import datetime
from pathlib import Path
from pydantic import BaseModel, FilePath
from typing import Union
from common.config import data_path

class FeedingRecord(BaseModel):
    feeding_dates: datetime

def load_or_initialize_feedings(file_path: Path) -> pd.DataFrame:
    """
    Load the feeding data from a CSV file, or initialize a new DataFrame if the file does not exist.

    :param file_path: The file path to load the data from.
    :return: A DataFrame containing the feeding dates.
    """
    if file_path.exists():
        return pd.read_csv(file_path, parse_dates=["feeding_dates"])
    return pd.DataFrame({"feeding_dates": pd.Series([], dtype="datetime64[ns]")})

def add_feeding_date(feeding_date: datetime, file_path: Path) -> pd.DataFrame:
    """
    Adds a feeding date to the DataFrame and saves it to a CSV file.

    :param feeding_date: The feeding date to add.
    :param file_path: The file path to save the data to.
    :return: The updated DataFrame.
    """
    feedings = load_or_initialize_feedings(file_path)
    new_entry = pd.DataFrame({"feeding_dates": [feeding_date]})
    updated_feedings = pd.concat([feedings, new_entry], ignore_index=True)
    updated_feedings.to_csv(file_path, index=False)
    return updated_feedings

def update_feedings(date_str: str, file_path: Union[Path, str] = data_path) -> pd.DataFrame:
    """
    Main function to update feedings with a new date.

    :param date_str: The date string to add, in 'YYYY-MM-DD' format.
    :param file_path: The data path where the feedings.csv is stored or should be saved.
    :return: The updated DataFrame.
    """
    date_object = datetime.strptime(date_str, "%Y-%m-%d")
    feedings_file_path = Path(file_path) / "feedings.csv"
    updated_feedings = add_feeding_date(date_object, feedings_file_path)
    return updated_feedings
