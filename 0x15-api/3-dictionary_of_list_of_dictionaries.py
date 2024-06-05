#!/usr/bin/python3
"""
This module fetches and exports the TODO list
for all employees from JSONPlaceholder API.
It exports the TODO list to a JSON file.

Usage:
    python script.py

The script does not expect any command-line arguments.
"""

import json
import requests


def fetch_all_employees_todo():
    """
    Fetches the TODO list for all employees and exports it to a JSON file.

    Raises:
        requests.RequestException: If there is an error with the HTTP request.
        KeyError: If expected data is missing in the API response.
        Exception: For any other unexpected errors.
    """
    try:
        # Fetch all users data
        users_response = requests.get(
                'https://jsonplaceholder.typicode.com/users')
        users_response.raise_for_status()
        users_data = users_response.json()

        # Fetch all todos data
        todos_response = requests.get(
                'https://jsonplaceholder.typicode.com/todos')
        todos_response.raise_for_status()
        todos_data = todos_response.json()

        # Organize tasks by user
        todos_by_user = {}
        for user in users_data:
            user_id = user.get('id')
            username = user.get('username')
            user_todos = [task for task in todos_data if task.get(
                                                        'userId') == user_id]
            todos_by_user[user_id] = [
                {
                    "username": username,
                    "task": task.get('title'),
                    "completed": task.get('completed')
                } for task in user_todos
            ]

        # Export data to JSON
        json_filename = 'todo_all_employees.json'
        with open(json_filename, 'w') as json_file:
            json.dump(todos_by_user, json_file, indent=4)

    except requests.RequestException as e:
        print(f"An error occurred: {e}")
    except KeyError as e:
        print(f"Missing expected data: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    """
    Main entry point of the script.

    Fetches and exports the TODO list for all employees to a JSON file.
    """
    fetch_all_employees_todo()
