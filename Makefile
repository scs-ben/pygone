pygone: pygone.py
	mkdir ./dist && python3 pyshrink.py && python3 shrink.py && python3 combine.py pygone-final.py > ./dist/pygone && chmod +x ./dist/pygone && xz -z ./dist/pygone && rm pygone-combined.py && rm pygone-final.py && rm pygone-mini.py && rm -f ./dist/pygone~ && ./prepare.sh && ls -l ./dist/pygone
