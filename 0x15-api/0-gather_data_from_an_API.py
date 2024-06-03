#!/usr/bin/python3

import requests
import sys

'''
 A python script that uses api to fetch
 information about an employee
'''


def get_employee_todo_progress(employee_id):
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
    if len(sys.argv) != 2:
        print("Usage: python 0-gather_data_from_an_API.py <employee_id>")
        sys.exit(1)

    try:
        employee_id = int(sys.argv[1])
        get_employee_todo_progress(employee_id)
    except ValueError:
        print("The employee ID must be an integer.")
        sys.exit(1)
