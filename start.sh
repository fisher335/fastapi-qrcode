#!/bin/sh
 
pid=`ps -ef|grep "python -u run.py"| grep -v "grep"|awk '{print $2}'`
 
if [ "$pid" != "" ]
then
        echo "run.py already run, stop it first"
        kill -9 ${pid}
fi
 
echo "starting now..."
 
nohup python -u main.py > test.out 2>&1 &
 
pid=`ps -ef|grep "python -u run.py"| grep -v "grep"|awk '{print $2}'`
 
echo ${pid} > pid.out
echo "run.py started at pid: "${pid}