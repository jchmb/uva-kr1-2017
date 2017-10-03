import matplotlib.pyplot as plt

to = 50
x = list(range(3, to+1))

avg = []
variables = []
total_clauses = []
ratio = []
nonbinary = []

for n in x:
    k = sum(list(range(n)))
    avg.append((n + 8*k)/(4*k + 1))
    variables.append(n**3)
    total_clauses.append(n**3*(4*k + 1))
    ratio.append((4*k+1)/n)
    nonbinary.append(1/(4*k + 1))


fig, (ax1, ax2) = plt.subplots(2, sharex=True)
plt.suptitle('Properties of DIMECS encoding as function of size N')

ax1.plot(x, avg, label='Avg clause length')
# ax1.plot(x, nonbinary, label='Non binary clauses')

ax2.plot(x, total_clauses, label='Clauses')
ax2.plot(x, variables, label='Variables')
ax2.plot(x, ratio, label='Ratio clauses/variables')
ax2.set_yscale('log')

legend = ax2.legend(loc='upper left')
legend = ax1.legend(loc='upper right')
ax1.set_xlim(2, to)
plt.show()
