from datetime import datetime
from matplotlib.collections import LineCollection
import matplotlib.pyplot as plt
import pylab
import sys

labeled = sys.argv[1:] == ['labeled']

raw = [x.split('\t') for x in open('data.txt').read().strip().split('\n')]

# Shortcut for parsing a formatted date to a timestamp.
timestamp = lambda x: (lambda y: datetime.strptime(y, x).timestamp())

# Parse the raw text data.
data = []
for name,gender,birth,start,death,a_start,a_end in raw:
    data.append((
        name,
        gender if gender in ('M', 'F') else '-',
        *map(timestamp('%Y-%m-%d'), (birth, start, death)),
        float(a_start),
        float(a_end)
    ))

# Draw line segments.
segments = {'M': [], 'F': [], '-': []}
for name,gender,birth,start,death,a_start,a_end in data:
    start = min(start, start - (a_start - 110)*365*86400)
    a_start = min(110, a_start)
    segments[gender].append(((start, a_start), (death, a_end)))

figure, ax = plt.subplots(figsize=(80 if labeled else 20, 20 if labeled else 5))
for g, color in (('M', 'blue'), ('F', 'magenta'), ('-', 'gray')):
    ax.add_collection(LineCollection(segments[g], linewidth=2, color=color))
    ends = [c[1] for c in segments[g]]
    plt.scatter([c[0] for c in ends], [c[1] for c in ends], color=color)

ax.autoscale()
ax.margins(0.1)

# Draw major and minor ticks, and grid.
years = list(map(timestamp('%Y'), map(str, range(1960, 2021, 5))))
years_minor = list(map(timestamp('%Y'), map(str, range(1960, 2021))))
plt.xticks(years, range(1960, 2021, 5))
ax.set_xticks(years_minor, minor=True)
plt.grid()

plt.savefig('bigplot.svg')
