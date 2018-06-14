#!/bin/bash
set -e

if [ $# -lt 2 ]
then
	echo "Need the package name and app name as input"
	exit 1
fi

pkgname=${1}
appname=${2}

echo "Current running workers process ids are"
pr=$(ps aux | grep -v stopgunicorn | grep gunicorn | grep $
{pkgname} | grep ${appname} | awk '{ print $2 }')


if [ "${pr}" != "" ]
then
	echo killing processes "${pr}"
	kill -9 ${pr} # will kill all of the workers
	echo "killed all the processes"
else
	echo "No gunicorn process found"
fi

echo validate if any more worker process in queue.

echo $(ps aux | grep -v stopgunicorn | grep gunicorn | grep ${pkgname} | grep ${appname})
echo "You should not see any process details above"

