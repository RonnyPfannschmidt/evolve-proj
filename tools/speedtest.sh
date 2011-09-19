function pypy-bin() {
    /home/ronny/Projects/pypy/pypy-bin/bin/pypy $@
}

for py in pypy-bin python
do
    for code in "visit" "code"
    do
        echo -n $py $code
        time {
            PYTHONPATH=../pyevolve $py funfind.py $code >/dev/null
        }
    done
done
