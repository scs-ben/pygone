sed -i '2s/^/gztmpdir=\/tmp\/$0\n/' pygone
sed -i '3s/^/tail -n +6 <"$0" | gzip -cd > "$gztmpdir"\n/' pygone
sed -i '4s/^/chmod a+x "$gztmpdir" && python3.8 "$gztmpdir"\n/' pygone
sed -i '5s/^/exit0\n/' pygone