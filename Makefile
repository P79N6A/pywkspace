all: env diff_run

env:
	sh build.sh

diff_run:
	source env/bin/activate && \
        python diff_run.py
