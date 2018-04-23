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
        gender,
        *map(timestamp('%Y-%m-%d'), (birth, start, death)),
        float(a_start),
        float(a_end)
    ))

# Draw line segments.
segments = []
for name,gender,birth,start,death,a_start,a_end in data:
    segments.append(((start, a_start), (death, a_end)))

width = 4 if labeled else 2
plot = LineCollection(segments, linewidth=width, color='red')

figure, ax = plt.subplots(figsize=(80 if labeled else 20, 20 if labeled else 5))
ax.add_collection(plot)
ax.autoscale()
ax.margins(0.1)

# Draw major and minor ticks, and grid.
years = list(map(timestamp('%Y'), map(str, range(1960, 2021, 5))))
years_minor = list(map(timestamp('%Y'), map(str, range(1960, 2021))))
plt.xticks(years, range(1960, 2021, 5))
ax.set_xticks(years_minor, minor=True)
plt.grid()

# Minimum duration before a label is shown.
label_threshold = 0 if labeled else 100

for name, gender, birth, start, death, a_start, a_end in data:
    parts = name.split()
    label = ' '.join([part[0] for part in parts[:-1]] + parts[-1:])
    duration = a_end - a_start
    if duration > label_threshold:
        xy = ((start + death) / 2, (a_start + a_end) / 2)
        xytext = (0, -20 * duration**0.75 - 20)
        plt.annotate(
            label,
            xy=xy, xytext=xytext,
            rotation=45,
            fontsize=5 + 3 * duration**0.75,
            textcoords='offset points', ha='center', va='top',
            arrowprops=dict(
                width=0.01, headlength=3, headwidth=3,
                color='grey', shrink=0.1, connectionstyle='arc3,rad=0'
            )
        )

plt.savefig('plot-{}labeled.svg'.format('' if labeled else 'un'))
