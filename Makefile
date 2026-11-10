.PHONY: pygone test bench regression

pygone: pygone.py
	mkdir -p ./dist && python3 pyshrink.py && python3 shrink.py && python3 combine.py pygone-final.py ./dist/pygone && chmod +x ./dist/pygone && xz -9 --check=none -z ./dist/pygone && rm pygone-combined.py && rm pygone-final.py && rm pygone-mini.py && rm -f ./dist/pygone~ && ./prepare.sh && test "$$(wc -c < ./dist/pygone)" -le 4096 && ls -l ./dist/pygone

test:
	printf 'unit\nquit\n' | python3 pygone.py

bench:
	printf 'position startpos\ngo depth 6\nquit\n' | python3 pygone.py

regression:
	./test/reg_test.sh
