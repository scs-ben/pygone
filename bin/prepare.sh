sed -i '1,48d' ./pygone
sed -i '1s/^/#!\/bin\/bash\n/' ./pygone
sed -i '2s/^/E=\/tmp\/$$\n/' ./pygone
sed -i '3s/^/tail -n +7 $0 | gunzip -c -q > $E\n/' ./pygone
sed -i '4s/^/chmod +x $E\n/' ./pygone
sed -i '5s/^/(sleep 5;rm $E)\&\n/' ./pygone
sed -i '6s/^/exec $E\n/' ./pygone
sed -i -e '$a\' ./pygone
echo >> ./pygone