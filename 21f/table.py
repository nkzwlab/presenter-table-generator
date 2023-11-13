from collections import namedtuple
from dataclasses import dataclass
import sys
import csv
import datetime

skip_people = ["nobody", "shanshang"]

if len(sys.argv) < 2:
    file = sys.stdin

else:
    file = open(sys.argv[1], 'r')


@dataclass
class Presenter:
    name: str
    title: str
    order: int = 0


presenters = [Presenter("nobody", "", 0)]
with open('./presenters.md', 'r') as f:
    for row in f:
        [_, name, title, *_] = row.split("|")
        name = name.strip()
        title = title.replace("<", "")
        title = title.replace(">", "")
        p = Presenter(name, title, order=-1)
        presenters.append(p)


reader = csv.reader(file)
for order, row in enumerate(reader, 1):
    person_number = int(row[0])

    presenter = presenters[person_number]
    presenter.order = order

sorted_presenters = sorted(presenters, key=lambda x: x.order)

time = datetime.datetime.now()
time = time.replace(hour=11, minute=15)

term_delta = datetime.timedelta(minutes=15)
wip_delta = datetime.timedelta(minutes=10)

ohiru = datetime.time(hour=12, minute=30)
ohiru_kyukei = datetime.timedelta(minutes=30)

#kyukei = [datetime.time(hour=14, minute=30), datetime.time(hour=16, minute=15)]
kyukei = [datetime.time(hour=14, minute=30)]
#kyukei = []
kyukei_delta = datetime.timedelta(minutes=15)

kyukeis = [(ohiru, ohiru_kyukei, "お昼休憩")] + \
    [(kk, kyukei_delta, "休憩") for kk in kyukei]

for presenter in sorted_presenters:
    if presenter.name in skip_people:
        continue

    print(f"| {presenter.order} | {time.strftime('%H:%M')} | {presenter.name} | {presenter.title} |")
    time = time + term_delta

    if kyukeis and time.time() >= kyukeis[0][0]:
        start = time
        end = time + kyukeis[0][1]
        print(
            f"|  | {start.strftime('%H:%M')} - {end.strftime('%H:%M')} | {kyukeis[0][2]} |  |")
        time = end
        kyukeis.pop(0)
