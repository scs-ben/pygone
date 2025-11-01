pygone: pygone.py
	python3 pyshrink.py && python3 shrink.py && python3 combine.py pygone-mini.py > ../bin/pygone && chmod +x ../bin/pygone && xz -z ../bin/pygone && rm pygone-mini.py && rm pygone-combined.py && rm -f ../bin/pygone~ && cd ../bin && ./prepare.sh && ls -l pygone
