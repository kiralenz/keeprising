import json
from typing import List, Union
from pathlib import Path
import pandas as pd
from common.config import feedings_path


def read_feedings() -> List[str]:
    """
    Reads the feedings from a JSON file. If the file doesn't exist, returns an empty list.

    :param file_path: The path to the feedings JSON file.
    :return: A list of feeding dates.
    """
    try:
        with open(feedings_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def write_feedings(data: List[str]) -> None:
    """
    Writes the feedings to a JSON file.

    :param file_path: The path to the feedings JSON file.
    :param data: A list of feeding dates to write.
    """
    with open(feedings_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)

def add_feeding_date(feeding_date: str) -> None:
    """
    Adds a feeding date to the feedings JSON file.

    :param file_path: The path to the feedings JSON file.
    :param feeding_date: The feeding date to add.
    """
    data = read_feedings()
    # converting date to string to store in JSON
    feeding_date = feeding_date.strftime("%Y-%m-%d")
    data.append(feeding_date)
    write_feedings(data=data)


def prepare_feedings_into_df() -> pd.DataFrame:
    """
    Converts a list of feeding dates into a pandas DataFrame,
    removes duplicates, sorts by date, and resets the index.

    :param file_path: The file path to the feedings JSON file.
    :return: A processed DataFrame of feeding dates.
    """
    # Read feeding dates from JSON file
    feedings_list = read_feedings()

    # Convert the list into a DataFrame
    df = pd.DataFrame(feedings_list, columns=['date'])

    # Remove duplicate entries
    df.drop_duplicates(inplace=True)

    # Sort the DataFrame by date
    df.sort_values(by='date', inplace=True)

    # Reset the index of the DataFrame
    df.reset_index(drop=True, inplace=True)

    return df

def update_feedings(feeding_date: str) -> pd.DataFrame:
    """
    Adds a feeding date to the JSON file and returns the updated list of feedings as a pandas DataFrame.

    :param file_path: The file path to the feedings JSON file.
    :param feeding_date: The feeding date to add, as a string.
    :return: A pandas DataFrame containing the updated list of feedings, processed to remove duplicates,
             sorted by date, and with the index reset.
    """
    # Add the feeding date to the JSON file
    add_feeding_date(feeding_date=feeding_date)

    # Prepare and return the updated feedings as a DataFrame
    return prepare_feedings_into_df()

