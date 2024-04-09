import json
from typing import List, Union
from pathlib import Path
import pandas as pd


def read_feedings(file_path: Union[str, Path]) -> List[str]:
    """
    Reads the feedings from a JSON file. If the file doesn't exist, returns an empty list.

    :param file_path: The path to the feedings JSON file.
    :return: A list of feeding dates.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def write_feedings(file_path: Union[str, Path], data: List[str]) -> None:
    """
    Writes the feedings to a JSON file.

    :param file_path: The path to the feedings JSON file.
    :param data: A list of feeding dates to write.
    """
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)

def add_feeding_date(file_path: Union[str, Path], feeding_date: str) -> None:
    """
    Adds a feeding date to the feedings JSON file.

    :param file_path: The path to the feedings JSON file.
    :param feeding_date: The feeding date to add.
    """
    data = read_feedings(file_path)
    data.append(feeding_date)
    write_feedings(file_path, data)


def prepare_feedings_df(file_path: Union[str, Path]) -> pd.DataFrame:
    """
    Converts a list of feeding dates into a pandas DataFrame,
    removes duplicates, sorts by date, and resets the index.

    :param file_path: The file path to the feedings JSON file.
    :return: A processed DataFrame of feeding dates.
    """
    # Read feeding dates from JSON file
    feedings_list = read_feedings(file_path)

    # Convert the list into a DataFrame
    df = pd.DataFrame(feedings_list, columns=['date'])

    # Remove duplicate entries
    df.drop_duplicates(inplace=True)

    # Sort the DataFrame by date
    df.sort_values(by='date', inplace=True)

    # Reset the index of the DataFrame
    df.reset_index(drop=True, inplace=True)

    return df

# to do
def update_feedings(feedings_df: pd.DataFrame, feeding_date: str) -> pd.DataFrame:
    pass
    # add feeding date
    # get new df