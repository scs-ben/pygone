pygone: pygone.py
	bash shrink.sh && pyminifier -o pygone-mini.py pygone-shrink.py && python3.8 combine.py pygone-mini.py > ../bin/pygone && chmod +x ../bin/pygone && gzexe ../bin/pygone && ls -l ../bin/pygone && rm ../bin/pygone~
