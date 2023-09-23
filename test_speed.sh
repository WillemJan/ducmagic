echo "Initial"
/usr/bin/time -o time (duc index / > /dev/null; ducmagic index / > /dev/null; ducmagic ls / > /dev/null)
(echo "Initial time to index with DUC and ducmagic"; cat time) | cowsay
echo "Cache"
/usr/bin/time -o time (ducmagic ls / > /dev/null)
(echo "Cached ducmagic call."; cat time) | cowsay
