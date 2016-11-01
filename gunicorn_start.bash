#!/bin/bash

PORT=8000
NAME="loan_app"                                  # Name of the application
USER=`whoami`                                        # the user to run as
NUM_WORKERS=2                                     # how many worker processes should Gunicorn spawn
FLASK_DIR=.

echo "Starting $NAME as `whoami`"

# Activate the virtual environment
cd $FLASK_DIR
source ~/.virtualenvs/loanenv/bin/activate
export PYTHONPATH=$FLASK_DIR:$PYTHONPATH

# Create the run directory if it doesn't exist
#RUNDIR=$(dirname run)
#test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec gunicorn runserver:app \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER \
  --bind=127.0.0.1:$PORT \
  --log-level=debug \
  --log-file=-


