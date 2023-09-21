echo "Initial run"
time (find . -type d && find . -type f -exec file '{}' ';'; find . -type f -exec ls -s '{}' ';') > /dev/null
echo 
echo "Second run"
time (find . -type d && find . -type f -exec file '{}' ';'; find . -type f -exec ls -s '{}' ';') > /dev/null

#Initial run

#real	0m0,453s
#user	0m0,359s
#sys	0m0,095s

#Second run

#real	0m0,454s
#user	0m0,333s
#sys	0m0,121s
