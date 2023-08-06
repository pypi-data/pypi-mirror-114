import sys
import json
from typing import Any, Dict, List, Tuple
from urllib import request


NUM_OF_TASKS_THRESHOLD = 100 # 100 tasks
RUNNING_TIME_THRESOLD = 30000000000 # 30 seconds


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
    check, host, node_name = validate_args(args)
    host = host if host.endswith("/") else host + "/"

    tasks_endpoint = host + "_tasks/"
    data = fetch_json(tasks_endpoint)

    if check == "num-of-tasks":
        num_of_tasks(data, node_name)
    elif check == "longest-running-task":
        longest_running_task(data, node_name)
    else:
        sys.exit(126)


def read_cmd_args() -> List[str]:
    """
    Read cmd args. Exit with code 126 if the number of args is less than 2

    Returns:
        List[str]: [description]
    """
    args = sys.argv[1:]
    if len(args) < 3:
        sys.exit(126)
    return args


def validate_args(args: List[str]) -> Tuple[str, str, str]:
    """
    Validates cmd arguments

    Args:
        args (List[str]): list of cmd arguments

    Returns:
        (Tuple[str, str, str]): check to make, host, node name
    """
    # Read check to make
    check = args[0]
    if check not in ["num-of-tasks", "longest-running-task"]:
        sys.exit(126)

    # Get host from cmd arguments, then build endpoint str
    host = args[1]
    if not host.startswith("http"):
        sys.exit(126)

    # Get node
    node = args[2]

    return check, host, node


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
        data = response.read().decode("utf-8")
        return json.loads(data)
    except:
        sys.exit(3)


def num_of_tasks(data: Dict[str, Any], node_name: str) -> None:
    """
    Reads total number of tasks in node.
    Returns 1 if it's greater than the threshold (defaults to 1).

    Args:
        data (Dict[str, Any]): _tasks data
        node_name (str): node name
    """
    nodes = data.get("nodes", [])
    total_tasks = sum([
        len(node.get("tasks", {}))
        for _, node in nodes.items()
        if node.get("name", "") == node_name
    ])

    print(f"total number of tasks in {node_name}", total_tasks)

    if total_tasks > NUM_OF_TASKS_THRESHOLD:
        sys.exit(1)
    else:
        sys.exit(0)


def longest_running_task(data: Dict[str, Any], node_name: str) -> None:
    """
    Reads longest running task in node.
    Returns 1 if it's greater than the threshold (defaults to 1 second).

    Args:
        data (Dict[str, Any]): [description]
    """
    nodes = data.get("nodes", [])
    longest_running = max([
        task.get("running_time_in_nanos")
        for _, node in nodes.items()
        if node.get("name", "") == node_name
        for _, task in node.get("tasks", {}).items()
    ])

    print(f"longest running task in {node_name}", longest_running)

    if longest_running > RUNNING_TIME_THRESOLD:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
