echo "Initial"
export TIME="\t%E,\t%k"
echo "" > time
echo "" > time
/usr/bin/time -a -o time duc index / > /dev/null
echo "" >> time
/usr/bin/time -a -o time ducmagic index / > /dev/null
echo "" >> time
/usr/bin/time -a -o time ducmagic ls / > /dev/null
(echo "Initial time to index with DUC and ducmagic"; cat time) | cowsay -f /usr/share/cowsay/cows/ren.cow
echo "Cache"
/usr/bin/time -o time ducmagic ls / > /dev/null
(echo "Cached ducmagic call."; cat time) | cowsay -f /usr/share/cowsay/cows/ren.cow


time find / -exec file '{}' ';'
time ducmagic ls /
