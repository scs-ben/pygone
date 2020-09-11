sed -i '2,48d' ../bin/pygone
sed -i '2s/^/gztmpdir=\/tmp\/$0\n/' ../bin/pygone
sed -i '3s/^/tail -n +6 <"$0" | gzip -cd > "$gztmpdir"\n/' ../bin/pygone
sed -i '4s/^/chmod a+x "$gztmpdir" \&\& python3.8 "$gztmpdir"\n/' ../bin/pygone
sed -i '5s/^/exit 0\n/' ../bin/pygone