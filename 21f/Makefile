.PHONY: mention presentations

mentions: term-order.csv
	 grep -v name term-order.csv | cut -d, -f1 | sort | sed 's/^/@/' | nl | sed 's/^ *//g; s/\t/. /g'

presentations: term-order.csv
	grep -v name term-order.csv | cut -d, -f1 | sort | while read p
	do
		echo "| $$p | [<発表タイトル>](./jnok_term-final/$p) |    |";
	done
