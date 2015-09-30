#!/bin/sh

./mutilator.py &
./taskmaster.py &
while [ true ]; do
ls -l samples/ | wc -l ;
ls -l work/crash/ ;
sleep 1
clear
done
