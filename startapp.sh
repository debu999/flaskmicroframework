#!/bin/bash
set -e

if [ $# -lt 3 ]
then
	echo "To start application please provide parameters in following format."
	echo "startapp.sh pkgname.wsgimodulename server:port applicationname [numberofworkers]"
	exit 1
fi

{
readarray -d . -t arr <<< "${1}"
pkgname=$(echo ${arr[0]} | xargs)
modulename=$(echo ${arr[1]} | xargs)
}||{
echo Please check our first input its not in format pkgname.wsgimodulename
echo Received parameter is ${1}
}
{
readarray -d : -t arr <<< "${2}"
svrname=$(echo ${arr[0]} | xargs)
port=$(echo ${arr[1]} | xargs)
}||{
echo Please check our second input its not in format servername:port
echo Received parameter is ${2}
}

echo -e "System received the following parameters\n1.PackageName: ${pkgname}\n2.ModuleName: ${modulename}"
applicationname=${3}
numofworkers=${4}

if [ -z ${numofworkers} ]
then
    echo "3.NumberofWorkers(Default): 1"
    numofworkers=1
else
    echo "3.NumberofWorkers: ${numofworkers}"
fi
echo -e "4.ServerName: ${svrname}\n5.PortNumber: ${port}\n6.ApplicationName: ${applicationname}"
echo Starting the application ${pkgname}.${modulename} with gunicorn server binding at ${svrname}.${port}

pr=$(ps aux | grep -v "stopapp.sh\|startapp.sh" | grep gunicorn | grep ${pkgname}.${modulename} | awk '{ print $2 }')

if [ "${pr}" != "" ]
then
	echo Stopping current application processes for the application "${pkgname}.${modulename}"
	$(pwd)/stopapp.sh ${pkgname}.${modulename}
	echo "System will spawn new processes."
else
	echo -e "No current process running for application ${pkgname}.${modulename}.\nSystem will spawn new processes."
fi

if [ ${numofworkers} -lt 2 ]
then
    echo gunicorn -b ${svrname}:${port} ${pkgname}.${modulename}:application
    gunicorn -b ${svrname}:${port} ${pkgname}.${modulename}:application --access-logfile - --error-logfile - --log-file - --log-level debug --capture-output --enable-stdio-inheritance
else
    echo gunicorn -w ${numofworkers} -D -b ${svrname}:${port} ${pkgname}.${modulename}:application
    gunicorn -w ${numofworkers} -b ${svrname}:${port} ${pkgname}.${modulename}:application --access-logfile - --error-logfile - --log-file - --log-level debug --capture-output --enable-stdio-inheritance
fi

sleep .5
echo validate gunicorn processes started in the system.
ps aux | grep -v "stopapp.sh\|startapp.sh\grep" | grep gunicorn | grep ${pkgname}.${modulename}
echo "Web application started successfully with ${numofworkers} worker nodes and 1 masternode"

