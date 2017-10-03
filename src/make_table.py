import compute_statistics
from argparse import ArgumentParser


parser = ArgumentParser(description='Draw a plot of a given statistic')
parser.add_argument('filename', type=str, help='Filename of the data source')
args = parser.parse_args()

filename = args.filename
aggregate = compute_statistics.aggregate_statistics(filename)
fields = ['propagations', 'decisions', 'cpu_time', 'conflicts', 'clauses']
# fields = 'propagations
# ,restarts,decisions,conflict_literals,variables,cpu_time,conflicts,clauses '

result = 'N,M,Smart,'
for field in fields:
    result += field+',,'
result += '\n'


result += ',,,' + 'mean,std,' * len(fields) + '\n'
for n in range(3, 16):
    first_in_n = True
    for m in range(10, 100, 10):
        first_in_m = True
        for s in [True, False]:
            row = ''
            if first_in_n:
                first_in_n = False
                row += str(n)
            row += ','
            if first_in_m:
                first_in_m = False
                row += str(m)
            row += ',' + str(s) + ','
            for field in fields:
                last = field == fields[-1]
                if (n, m, s) in aggregate[field]:
                    stats = aggregate[field][(n, m, s)]
                    mean = round(stats['mean'], 2)
                    stddev = round(stats['var'], 2)
                else:
                    (mean, stddev) = ('-', '-')
                row += str(mean) + ',' + str(stddev)
                if not last:
                    row += ','
            row += '\n'
            result += row

print(result)
