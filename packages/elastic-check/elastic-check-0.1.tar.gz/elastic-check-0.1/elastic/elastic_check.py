import sys
import json
from typing import Any, Dict, List, Tuple
from urllib import request


NUM_OF_TASKS_THRESHOLD = 1500
RUNNING_TIME_THRESOLD = 60000000000


def run() -> None:
    """
    elastic-check entrypoint
    """
    main()


def main() -> None:
    """
    Main entrypoint
    """
    args = read_cmd_args()
    check, host = validate_args(args)
    host = host if host.endswith("/") else host + "/"

    tasks_endpoint = host + "_tasks/"
    data = fetch_json(tasks_endpoint)

    if check == "num-of-tasks":
        num_of_tasks(data)
    elif check == "longest-running-task":
        longest_running_task(data)
    else:
        sys.exit(126)


def read_cmd_args() -> List[str]:
    """
    Read cmd args. Exit with code 126 if the number of args is less than 2

    Returns:
        List[str]: [description]
    """
    args = sys.argv[1:]
    if len(args) < 2:
        sys.exit(126)
    return args


def validate_args(args: List[str]) -> Tuple[str, str]:
    """
    Validates cmd arguments

    Args:
        args (List[str]): list of cmd arguments

    Returns:
        (Tuple[str]): check to make, host
    """
    # Read check to make
    check = args[0]
    if check not in ["num-of-tasks", "longest-running-task"]:
        sys.exit(126)

    # Get host from cmd arguments, then build endpoint str
    host = args[1]
    if not host.startswith("http"):
        sys.exit(126)

    return check, host


def fetch_json(url: str) -> Dict[str, Any]:
    """
    Makes a request and parses its response.

    Args:
        url (str): url

    Returns:
        Dict[str, Any]: parsed response
    """
    try:
        response = request.urlopen(url)
        data = response.read().decode('utf-8')
        return json.loads(data)
    except:
        sys.exit(1)


def num_of_tasks(data: Dict[str, Any]) -> None:
    """
    Reads total number of tasks in cluster.
    Returns 1 if it's greater than the threshold (defaults to 1).

    Args:
        data (Dict[str, Any]): _tasks data
    """
    nodes = data.get("nodes", [])
    total_tasks = sum([
        len(node.get("tasks", {}))
        for _, node in nodes.items()
    ])
    print("total tasks", total_tasks)
    if total_tasks > NUM_OF_TASKS_THRESHOLD:
        sys.exit(1)
    else:
        sys.exit(0)


def longest_running_task(data: Dict[str, Any]) -> None:
    """
    Reads longest running task in cluster.
    Returns 1 if it's greater than the threshold (defaults to 1 second).

    Args:
        data (Dict[str, Any]): [description]
    """
    nodes = data.get("nodes", [])
    longest_running = max([
        task.get("running_time_in_nanos")
        for _, node in nodes.items()
        for _, task in node.get("tasks", {}).items()
    ])
    print("longest running task", longest_running)
    if longest_running > RUNNING_TIME_THRESOLD:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
