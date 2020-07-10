#!/bin/sh
cd /data/workflow-annualreportextractsub-etl
LOGS_DIR=logs

if [ ! -d "${LOGS_DIR}" ]
then
  mkdir "${LOGS_DIR}"
fi

python3 workflow-annualreportextractsub-etl.py workflow-annualreportextractsub-etl.conf $python_env

echo $python_env
echo "workflow-annualreportextractsub-etl.py starting..."
