SHELL=/bin/bash

.SHELLFLAGS=-eci
.ONESHELL:

OBJS=profile_output* __pycache__
CONDA_ENV=python-ipc


# CONDA ENVIRONMENT
environment: environment.yml
	-conda env remove -yn ${CONDA_ENV}
	conda env create -f environment.yml


# INDEPENDENT SOCKET TESTS / PROFILING
.PHONY: profile-socket-indep-ipc-remote profile-socket-indep-ipc-main

profile-socket-indep-ipc-remote:
	conda activate ${CONDA_ENV}
	export LINE_PROFILE=1 && python socket-indep-ipc-remote.py
	python -m line_profiler -rtmz profile_output.lprof

profile-socket-indep-ipc-main:
	conda activate ${CONDA_ENV}
	export LINE_PROFILE=1 && python socket-indep-ipc-main.py
	python -m line_profiler -rtmz profile_output.lprof


# UTILITIES
.PHONY: clean
clean:
	rm -rfv ${OBJS}
