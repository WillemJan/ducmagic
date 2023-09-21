for f in $(find .);do
    r=$(file "$f") 
    ft="$(echo $r | cut -d ":" -f 2)" 
    if [ "$ft" != " directory" ]; then 
        s=$(ls -s "$f"); 
        echo "$ft" "$s"
    else 
        echo "$ft" "$f" "0"
    fi
done
