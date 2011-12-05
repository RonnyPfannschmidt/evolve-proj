#!/bin/bash

function pypy-bin() {
    /home/ronny/Projects/pypy/pypy-bin/bin/pypy $@
}

TIMEFORMAT=$'  real %lE\n  user %lU\n  sys %lS'

for py in pypy-bin python
do
    for kind in stack visit code
    do
        echo $py $kind
        time {
            PYTHONPATH=../pyevolve $py funfind.py $kind >/dev/null
        }
    done
done
