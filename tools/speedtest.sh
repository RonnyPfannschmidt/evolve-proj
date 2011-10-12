function pypy-bin() {
    /home/ronny/Projects/pypy/pypy-bin/bin/pypy $@
}

for py in pypy-bin python
do
    for kind in stack visit code
    do
        echo -n $py $kind
        time {
            PYTHONPATH=../pyevolve $py funfind.py $kind >/dev/null
        }
    done
done
