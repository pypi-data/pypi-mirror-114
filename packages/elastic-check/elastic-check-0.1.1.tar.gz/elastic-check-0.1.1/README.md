# elastic-check

A small utility script used to monitor elastic nodes through the /_tasks/ endpoint.

It uses exit codes to express the result of the "check":
- Exit code 0: check completed successfully.
- Exit code 1: check failed (error).
- Exit code 3: network error (could not connect).
- Exit code 4: node not found.
- Exit code 126: invalid arguments.

*NOTE*: works with Python 3 only

## Install
```sh
pip3 install elastic-check
```

## How to use?
```sh
elastic-check <check> <host> <node_name>
```

Where _check_ can be:
- num-of-tasks: checks the number of tasks in the node and compares to threshold.
- longest-running-time: checks the longest running task and compares to threshold.

### Examples
```sh
elastic-check num-of-tasks http://elastic-cloud:9243 node01
```
```sh
elastic-check longest-running-time https://elastic-cloud.com:9243 node02
```