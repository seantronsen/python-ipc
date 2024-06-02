# python-ipc

Contained within this repository is a series of tests which I conducted against
the Python implementations for interprocesscommunication and/or data sharing.

## Terminology

- **Independent Processes**: Processes launched independently from one another.
  For an example, open a shell, start a process. Then open another shell and
  start a different process.

## Implementions Tested

- IPC between two independent processes using the `socket` package

## Implementations Remaining

- IPC between two processes using system pipes via the `subprocess` package
- IPC between two processes using pipes via the `multiprocessing` package
- IPC between two processes using queues from the `multiprocessing` package
- IPC using D-BUS communications

## Future Work

- A brief comparison between `multiprocessing` and `subprocess` to determine
  which should be used for the visualization / tuning program. 
- A review on PyQt's threading and process libraries with an additional look at
  their D-BUS communications library. 

