echo "Initial run"
/usr/bin/time -o time ((find . -type d && find . -type f -exec file '{}' ';'; find . -type f -exec ls -s '{}' ';') > /dev/null)
(echo "Initial run with bash and magic combined."; cat time) | cowsay
echo 
echo "Second run"
/usr/bin/time -o time ((find . -type d && find . -type f -exec file '{}' ';'; find . -type f -exec ls -s '{}' ';') > /dev/null)
(echo "Second run with bash and magic combined."; cat time) | cowsay
