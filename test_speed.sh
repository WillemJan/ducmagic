rm ~/.duc.db; rm ~/.duc_magic.db

echo "Initial"
time (duc index .; ducmagic index .; ducmagic ls) > /dev/null
echo
echo "Cache"
time (ducmagic ls) > /dev/null

#Initial

#real	0m0,150s
#user	0m0,208s
#sys	0m0,110s

#Cache

#real	0m0,051s
#user	0m0,043s
#sys	0m0,008s
