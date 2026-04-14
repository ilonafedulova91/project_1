from pathlib import Path

from utils import load_data
from views import events_page, main_page

PROJECT_DIR = Path(__file__).parent.parent


def run_main_page(file_path: str, date_str: str):
    """This function runs the main page of the website."""
    try:
        data = load_data(file_path)

        result = main_page(data, date_str)
        print(result)
    except Exception as e:
        print(f"Ошибка на главной странице: {e}")


def run_events_page(file_path: str, date_str: str, data_range: str = "M"):
    """This function runs the events page of the website."""
    try:
        data = load_data(file_path)

        result = events_page(data, date_str, data_range)
        print(result)
    except Exception as e:
        print(f'Ошибка на странице "События": {e}')


def main():
    """This is the main function."""
    file_path = f"{PROJECT_DIR}/data/operations.xlsx"
    date = "15.12.2023"
    data_range = "M"

    print("\n--- MAIN PAGE ---")
    run_main_page(file_path, date)

    print("\n--- EVENTS PAGE ---")
    run_events_page(file_path, date, data_range)


if __name__ == "__main__":
    main()
