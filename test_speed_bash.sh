echo "Initial run"

/usr/bin/time -o time `find / -type d > /dev/null 2>&1 && find / -type f -exec file '{}' > /dev/null 2>&1 ';' ; find / -type f -exec ls -s '{}' > /dev/null 2>&1 ';'` > /dev/null
(echo "Initial run with bash and magic combined."; cat time) | cowsay
echo

echo "Second run"
/usr/bin/time -o time `find / -type d > /dev/null 2>&1 && find / -type f -exec file '{}' > /dev/null 2>&1 ';'; find / -type f -exec ls -s '{}' > /dev/null 2>&1 ';'` > /dev/null
(echo "Second run with bash and magic combined."; cat time) | cowsay
