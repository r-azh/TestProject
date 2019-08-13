#!/usr/bin/env bash

#sleep 10 &
#PID=$!

python3 TestPython/test_encryption/test_encrypt.py &
PID=$!
echo $PID

while (kill -0 $PID > /dev/null 2>&1); do
    (echo  && ps -p $PID -e -o pcpu,pmem | cut -d" " -f1-5 | tail -n 1) >> ps.log;
    sleep 0.1;
done


#    (echo "%CPU %MEM " && ps -p $PID -e -o pcpu,pmem | cut -d" " -f1-5 | tail -n 1) >> ps.log;


# run ./TestPython/test_encryption/monitor.sh