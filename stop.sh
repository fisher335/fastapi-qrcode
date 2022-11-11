#!/bin/sh
 
pid=`ps -ef|grep "python -u run.py"| grep -v "grep"|awk '{print $2}'`
 
if [ "$pid" != "" ]
then
        kill -9 ${pid}
        echo "stop run.py complete"
else
        echo "run.py is not run, there's no need to stop it"
fi