#!/usr/bin/python3
"""
    Fetches and displays the TODO list progress for a given employee ID.

    Args:
        employee_id (int): The ID of the employee.

    Raises:
        requests.RequestException: If there is an error with the HTTP request.
        KeyError: If expected data is missing in the API response.
        Exception: For any other unexpected errors.
"""
import requests
import sys


def get_employee_todo_progress(employee_id):
    """
    Fetches and displays the TODO list progress for a given employee ID.
    Exports the TODO list to a CSV file.

    Args:
        employee_id (int): The ID of the employee.

    Raises:
        requests.RequestException: If there is an error with the HTTP request.
        KeyError: If expected data is missing in the API response.
        Exception: For any other unexpected errors.
    """
    try:
        # Fetch employee data
        user_response = requests.get(
                f'https://jsonplaceholder.typicode.com/users/{employee_id}')
        user_response.raise_for_status()
        user_data = user_response.json()

        # Fetch todos data
        todos_response = requests.get(
            f'https://jsonplaceholder.typicode.com/todos?userId={employee_id}')
        todos_response.raise_for_status()
        todos_data = todos_response.json()

        employee_name = user_data['name']
        total_tasks = len(todos_data)
        done_tasks = [task for task in todos_data if task['completed']]
        number_of_done_tasks = len(done_tasks)

        # Print the progress
        print(f"Employee {employee_name} is done with tasks\
({number_of_done_tasks}/{total_tasks}):")
        for task in done_tasks:
            print(f"\t {task['title']}")
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
    except KeyError as e:
        print(f"Missing expected data: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    """
    Main entry point of the script.

    Expects a single command-line argument which is the employee ID.
    Fetches and displays the TODO list progress of the specified employee and
    exports the data to a CSV file.

    Usage:
        python script.py <employee_id>
    """
    if len(sys.argv) != 2:
        print("Usage: python 0-gather_data_from_an_API.py <employee_id>")
        sys.exit(1)

    try:
        employee_id = int(sys.argv[1])
        get_employee_todo_progress(employee_id)
    except ValueError:
        print("The employee ID must be an integer.")
        sys.exit(1)
