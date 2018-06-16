#!/bin/bash
set -e

if [ $# -lt 1 ]
then
	echo "Need the package name and wsgimodule name as input to stop the application"
	echo "Format is packagename.modulename"
	exit 1
fi

readarray -d . -t arr <<< "${1}"

pkgname=$(echo ${arr[0]} | xargs)
modulename=$(echo ${arr[1]} | xargs)

pr=$(ps aux | grep -v "stopapp.sh\|startapp.sh" | grep gunicorn | grep ${pkgname}.${modulename} | awk '{ print $2 }')


if [ "${pr}" != "" ]
then
    echo -e "Current running workers process ids for application ${pkgname}.${modulename} are:\n${pr}. \nThese processes will be killed"
	kill -9 ${pr} # will kill all of the workers
	echo "killed all running processes under gunicorn for application ${pkgname}.${modulename}"
	echo validate if any more worker process in queue.
    echo $(ps aux | grep -v "stopapp.sh\|startapp.sh" | grep gunicorn | grep ${pkgname}.${modulename})
    echo "You should not see any process details above"
else
	echo "No gunicorn process found for application ${pkgname}.${modulename}"
fi

