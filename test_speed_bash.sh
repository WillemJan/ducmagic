echo "Initial run"
time (find . -type d && find . -type f -exec file '{}' ';'; find . -type f -exec ls -s '{}' ';')
echo 
echo "Second run"
time (find . -type d && find . -type f -exec file '{}' ';'; find . -type f -exec ls -s '{}' ';')
