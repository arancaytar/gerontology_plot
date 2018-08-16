from datetime import datetime
from dateutil.relativedelta import relativedelta
from matplotlib.collections import LineCollection
import matplotlib.pyplot as plt
import csv

# Shortcut for parsing a formatted date to a timestamp.
def parse_time(date_format):
    return lambda y: datetime.strptime(y, date_format) if y.strip() else None


def average_years(delta):
    return delta.total_seconds() / 86400 / 365.234


raw = list(csv.reader(open('data.csv', newline='')))
data_end = parse_time('%Y-%m-%d')('2015-01-01')

# Parse the raw text data.
data = []
for line in raw:
    birth, death = map(parse_time('%Y-%m-%d'), (line[2], line[3]))
    data.append({
        'name': line[1],
        'gender': line[9] if line[9] in ('M', 'F') else '-',
        'birth': birth,
        'death': death,
        'rank': int(line[7])
    })


# The GRG defines supercentenarians as those who were alive on their 110th birthday,
# irrespective of leap days. Thus, use relativedelta here.
min_age = relativedelta(years=110)
segments = {'M': [], 'F': [], '-': []}
last_oldest = None
bold_segments = {'M': [], 'F': [], '-': []}
dots = {'M': [], 'F': [], '-': []}
for item in data:
    start_date = item['birth'] + min_age
    if item['death'] and item['death'].year < 1960:
        continue
    # To properly compare people, we count age in average years of 365.234 days.
    start_age = average_years(start_date - item['birth'])
    end_date = item['death'] or data_end
    end_age = average_years(end_date - item['birth'])
    segment = ((start_date.timestamp(), start_age), (end_date.timestamp(), end_age))
    segments[item['gender']].append(segment)
    if item['death']:
        dots[item['gender']].append((item['death'].timestamp(), end_age))
#    if item['rank'] == 1:
    #    bold_start = (last_oldest or start_date)
    #    bold_start_age = average_years(bold_start - item['birth'])
    #    bold_segment = ((bold_start.timestamp(), bold_start_age), segment[1])
    #    bold_segments[item['gender']].append(bold_segment)
#        bold_segments[item['gender']].append(segment)
#        last_oldest = end_date

figure, ax = plt.subplots(figsize=(60, 15))
for g, color, dot in (('F', 'magenta', '#880088'), ('M', 'blue', '#000088'), ('-', 'gray', '#444444')):
    ax.add_collection(LineCollection(segments[g], linewidth=1, color=color))
    ax.add_collection(LineCollection(bold_segments[g], linewidth=4, color=color))
    plt.scatter([c[0] for c in dots[g]], [c[1] for c in dots[g]], color=dot, zorder=10)

ax.autoscale()
ax.margins(0.1)

# Draw major and minor ticks, and grid.
def year_timestamp(year):
    return parse_time('%Y')(year).timestamp()

years = list(map(year_timestamp, map(str, range(1960, 2016, 5))))
years_minor = list(map(year_timestamp, map(str, range(1960, 2016))))
plt.xticks(years, range(1960, 2016, 5))
ax.set_xticks(years_minor, minor=True)
plt.grid()

plt.savefig('bigplot.svg')
