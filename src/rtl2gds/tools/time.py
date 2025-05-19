import functools
import json
import os
import time
from datetime import datetime
from typing import Callable

# Save all step timing data in a global dictionary
time_data = {
    "steps": {},
    "summary": {"total_time": 0, "start_time": "", "end_time": ""},
}


def time_decorator(func: Callable) -> Callable:
    """Record the time taken by a function and store it in a global dictionary.
    Args:
        func (Callable): The function to be decorated.
    Returns:
        Callable: The wrapped function with timing functionality.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        step_name = kwargs.get("step_name", func.__name__)

        # Record the start time
        start_time = time.perf_counter()
        start_datetime = datetime.now().isoformat()

        try:
            result = func(*args, **kwargs)
            status = "success"
        except Exception as e:
            status = f"failed: {str(e)}"
            raise
        finally:
            # Record the end time
            end_time = time.perf_counter()
            end_datetime = datetime.now().isoformat()
            elapsed = end_time - start_time

            # Record the timing data
            time_data["steps"][step_name] = {
                "start_time": start_datetime,
                "end_time": end_datetime,
                "elapsed_seconds": elapsed,
                "status": status,
            }

            # If it's the first step, record the total start time
            if not time_data["summary"]["start_time"]:
                time_data["summary"]["start_time"] = start_datetime

            # Update the total time
            time_data["summary"]["end_time"] = end_datetime
            time_data["summary"]["total_time"] += elapsed

        return result

    return wrapper


def save_execute_time_data(result_dir: str, chip_name: str) -> str:
    """Save the execution time data to a JSON file.
    Args:
        result_dir (str): Directory to save the JSON file.
        chip_name (str): Name of the chip.
    Returns:
        str: Path to the saved JSON file.
    """
    os.makedirs(result_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_file = os.path.join(result_dir, f"evaluation/{chip_name}_execution_time_{timestamp}.json")

    with open(json_file, "w") as f:
        json.dump(time_data, f, indent=2)

    return json_file
