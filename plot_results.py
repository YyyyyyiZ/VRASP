import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
gap_1 = 0.1
gap_2 = 0.2
cplex_p0_cost = [321.00, 290.14, 330.00, 325.66, 298.31, 304.64, 312.00, 321.96, 318.00, 320.73]
cplex_p0_time = [132.73, 69.20, 35.03, 18.20, 47.38, 136.85, 48.90, 10.59, 330.37, 55.65]
cplex_p1_cost = [308.00, 280.14, 326.00, 313.66, 286.31, 300.64, 312.00, 310.96, 315.00, 316.73]
cplex_p1_time = [94378.95, 73957.44, 80921.37, 88489.21, 69580.46, 72581.36, 90002.71, 85439.67, 77584.31, 79653.92]
vns_p0_cost = [322.41, 290.14, 331.68, 326.66, 298.47, 306.02, 314.35, 324.00, 319.77, 320.74]
vns_p0_time = [466.26, 477.71, 474.09, 442.45, 440.91, 405.68, 442.84, 443.25, 399.86, 436.65]
vns_p1_cost = [309.43, 283.00, 328.67, 315.23, 287.30, 301.53, 313.57, 311.90, 316.77, 319.37]
vns_p1_time = [2401.01, 2111.83, 1977.22, 1967.78, 1988.16, 2011.05, 1972.20, 1964.53, 1831.03, 2381.01]


# CPLEX-P0 vs. VNS-P0
fig = plt.figure(figsize=(8, 6), dpi=300)
ax = fig.add_subplot(111)
lin1 = ax.plot(x, cplex_p0_cost, label='CPLEX', marker='o', color='dimgray', linestyle='')
lin2 = ax.plot(x, vns_p0_cost, label='VNS', marker='^', color='dimgray', linestyle='')
for i in range(len(x)):
    ax.plot((x[i] + gap_1, x[i] + gap_1), (cplex_p0_cost[i], vns_p0_cost[i]), marker='_', color='steelblue', linestyle='-')
    ax.text(x[i] + gap_2, (cplex_p0_cost[i] + vns_p0_cost[i])/2, '%.2f%%' % ((vns_p0_cost[i]-cplex_p0_cost[i])*100/vns_p0_cost[i]), color='steelblue', fontsize=13)
ax.set_xlim([0, 11])
ax.set_xlabel('Instance No.', fontsize=20)
ax.set_ylabel('Cost', fontsize=20)


lines = lin1 + lin2
labs = [label.get_label() for label in lines]
ax.legend(lines, labs)
plt.xticks(x)
plt.savefig('cost_cplex0_vns0.png', dpi=300)
plt.show()

fig = plt.figure(figsize=(8, 6), dpi=300)
ax = fig.add_subplot(111)
lin3 = ax.plot(x, cplex_p0_time, label='CPLEX', marker='o', color='gray', linestyle='-')
lin4 = ax.plot(x, vns_p0_time, label='VNS', marker='^', color='gray', linestyle=':')
ax.set_xlabel('Instance No.', fontsize=20)
ax.set_ylabel('Running Time', fontsize=20)
lines = lin3 + lin4
labs = [label.get_label() for label in lines]
ax.legend(lines, labs)
plt.xticks(x)
plt.savefig('time_cplex0_vns0.png', dpi=300)
plt.show()


# CPLEX-P1 vs. VNS-P1
fig = plt.figure(figsize=(8, 6), dpi=300)
ax = fig.add_subplot(111)
lin1 = ax.plot(x, cplex_p1_cost, label='CPLEX', marker='o', color='dimgray', linestyle='')
lin2 = ax.plot(x, vns_p1_cost, label='VNS', marker='^', color='dimgray', linestyle='')
for i in range(len(x)):
    ax.plot((x[i] + gap_1, x[i] + gap_1), (cplex_p1_cost[i], vns_p1_cost[i]), marker='_', color='steelblue', linestyle='-')
    ax.text(x[i] + gap_2, (cplex_p1_cost[i] + vns_p1_cost[i])/2, '%.2f%%' % ((vns_p1_cost[i]-cplex_p1_cost[i])*100/vns_p1_cost[i]), color='steelblue', fontsize=13)
ax.set_xlim([0, 11])
ax.set_xlabel('Instance No.', fontsize=20)
ax.set_ylabel('Cost', fontsize=20)
lines = lin1 + lin2
labs = [label.get_label() for label in lines]
ax.legend(lines, labs)
plt.xticks(x)
plt.savefig('cost_cplex1_vns1.png', dpi=300)
plt.show()

fig = plt.figure(figsize=(8, 6), dpi=300)
f, (ax3, ax) = plt.subplots(2, 1, sharex=True)
ax.plot(x, vns_p1_time, label='VNS', marker='^', color='gray', linestyle=':')
ax3.plot(x, cplex_p1_time, label='CPLEX', marker='o', color='gray', linestyle='-')
ax3.plot(x, vns_p1_time, label='VNS', marker='^', color='gray', linestyle=':')

ax3.set_ylim(68000, 95000)
ax.set_ylim(1800, 2500)
ax3.legend()
ax.set_xticks(x)

ax.spines['top'].set_visible(False)  # 边框控制
ax3.spines['bottom'].set_visible(False)  # 边框控制

d = 0.01
kwargs = dict(transform=ax3.transAxes, color='k', clip_on=False)
ax3.plot((-d, +d), (-d, +d), **kwargs)  # top-left diagonal
kwargs.update(transform=ax.transAxes, color='k')
ax.plot((-d, +d), (1 - d, 1 + d), **kwargs)  # bottom-left diagonal

plt.xlabel('Instance No.', fontsize=20)
plt.ylabel('Running Time', fontsize=20)

plt.tight_layout()
plt.savefig('time_cplex1_vns1.png', dpi=300)
plt.show()


# CPLEX-P0 vs. CPLEX-P1
fig = plt.figure(figsize=(8, 6), dpi=300)
ax = fig.add_subplot(111)
lin1 = ax.plot(x, cplex_p0_cost, label='P0', marker='o', color='dimgray', linestyle='')
lin2 = ax.plot(x, cplex_p1_cost, label='P1', marker='^', color='dimgray', linestyle='')
for i in range(len(x)):
    ax.plot((x[i] + gap_1, x[i] + gap_1), (cplex_p0_cost[i], cplex_p1_cost[i]), marker='_', color='steelblue', linestyle='-')
    ax.text(x[i] + gap_2, (cplex_p0_cost[i] + cplex_p1_cost[i])/2, '%.2f%%' % ((cplex_p0_cost[i]-cplex_p1_cost[i])*100/cplex_p0_cost[i]), color='steelblue', fontsize=13)
ax.set_xlim([0, 11])
ax.set_xlabel('Instance No.', fontsize=20)
ax.set_ylabel('Cost', fontsize=20)
lines = lin1 + lin2
labs = [label.get_label() for label in lines]
ax.legend(lines, labs)
plt.xticks(x)
plt.savefig('cost_cplex0_cplex1.png', dpi=300)
plt.show()

fig = plt.figure(figsize=(8, 6), dpi=300)
f, (ax3, ax) = plt.subplots(2, 1, sharex=True)
ax.plot(x, cplex_p0_time, label='P0', marker='^', color='gray', linestyle=':')
ax3.plot(x, cplex_p1_time, label='P1', marker='^', color='gray', linestyle='-')
ax3.plot(x, cplex_p0_time, label='P0', marker='o', color='gray', linestyle='-')

ax3.set_ylim(68000, 95000)
ax.set_ylim(10, 350)
ax3.legend()
ax.set_xticks(x)

ax.spines['top'].set_visible(False)  # 边框控制
ax3.spines['bottom'].set_visible(False)  # 边框控制

d = 0.01
kwargs = dict(transform=ax3.transAxes, color='k', clip_on=False)
ax3.plot((-d, +d), (-d, +d), **kwargs)  # top-left diagonal
kwargs.update(transform=ax.transAxes, color='k')
ax.plot((-d, +d), (1 - d, 1 + d), **kwargs)  # bottom-left diagonal

plt.xlabel('Instance No.', fontsize=20)
plt.ylabel('Running Time', fontsize=20)

plt.tight_layout()
plt.savefig('time_cplex0_cplex1.png', dpi=300)
plt.show()


# VNS-P0 vs. VNS-P1
fig = plt.figure(figsize=(8, 6), dpi=300)
ax = fig.add_subplot(111)
lin1 = ax.plot(x, vns_p0_cost, label='P0', marker='o', color='dimgray', linestyle='')
lin2 = ax.plot(x, vns_p1_cost, label='P1', marker='^', color='dimgray', linestyle='')
for i in range(len(x)):
    ax.plot((x[i] + gap_1, x[i] + gap_1), (vns_p0_cost[i], vns_p1_cost[i]), marker='_', color='steelblue', linestyle='-')
    ax.text(x[i] + gap_2, (vns_p0_cost[i] + vns_p1_cost[i])/2, '%.2f%%' % ((vns_p0_cost[i]-vns_p1_cost[i])*100/vns_p0_cost[i]), color='steelblue', fontsize=13)
ax.set_xlim([0, 11])
ax.set_xlabel('Instance No.', fontsize=20)
ax.set_ylabel('Cost', fontsize=20)
lines = lin1 + lin2
labs = [label.get_label() for label in lines]
ax.legend(lines, labs)
plt.xticks(x)
plt.savefig('cost_vns0_vns1.png', dpi=300)
plt.show()

fig = plt.figure(figsize=(8, 6), dpi=300)
f, (ax3, ax) = plt.subplots(2, 1, sharex=True)
ax.plot(x, vns_p0_time, label='P0', marker='^', color='gray', linestyle=':')
ax3.plot(x, vns_p1_time, label='P1', marker='o', color='gray', linestyle='-')
ax3.plot(x, vns_p0_time, label='P0', marker='^', color='gray', linestyle=':')

ax3.set_ylim(1800, 2500)
ax.set_ylim(390, 480)
ax3.legend(loc='upper right')
ax.set_xticks(x)

ax.spines['top'].set_visible(False)  # 边框控制
ax3.spines['bottom'].set_visible(False)  # 边框控制

d = 0.01
kwargs = dict(transform=ax3.transAxes, color='k', clip_on=False)
ax3.plot((-d, +d), (-d, +d), **kwargs)  # top-left diagonal
kwargs.update(transform=ax.transAxes, color='k')
ax.plot((-d, +d), (1 - d, 1 + d), **kwargs)  # bottom-left diagonal

plt.xlabel('Instance No.', fontsize=20)
plt.ylabel('Running Time', fontsize=20)

plt.tight_layout()
plt.savefig('time_vns0_vns1.png', dpi=300)
plt.show()
