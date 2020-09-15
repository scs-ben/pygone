sed -i '1,48d' ./pygone
sed -i '1s/^/#!\/bin\/bash\n/' ./pygone
sed -i '2s/^/tail -n NUMBER_OF_LINES $0 | gunzip -c -q > \/tmp\/$$\n/' ./pygone
sed -i '3s/^/chmod +x \/tmp\/$$\n/' ./pygone
sed -i '4s/^/\/tmp\/$$\n/' ./pygone
sed -i '5s/^/rm \/tmp\/$$\n/' ./pygone
sed -i '6s/^/exit0\n/' ./pygone
sed -i -e '$a\' ./pygone