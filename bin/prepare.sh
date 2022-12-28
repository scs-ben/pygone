sed -i '1s/^/#!\/bin\/sh\n/' ./pygone.xz
sed -i '2s/^/T=`mktemp`\n/' ./pygone.xz
sed -i '3s/^/tail -n +6 "$0"|xz -d>$T 2>\/dev\/null\n/' ./pygone.xz
sed -i '4s/^/chmod +x $T\n/' ./pygone.xz
sed -i '5s/^/(sleep 3;rm $T)\&exec $T\n/' ./pygone.xz
mv ./pygone.xz ./pygone
echo >> ./pygone