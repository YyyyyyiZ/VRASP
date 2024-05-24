import numpy as np
import pandas as pd
import scipy.stats as stats

df = pd.read_csv('data_0502_use.csv',index_col=0)

std_theta = 0

# 计算前912行的平均值
avg_values = df.head(912).mean()

# 将平均值作为新行添加到DataFrame中
df.loc['predict'] = avg_values

# epsilon1-epsilon9的标准差:  arr
std_epsilon = arr = [109.92, 109.923, 109.941, 109.954, 109.954, 109.956, 109.951, 109.943, 109.949]
sum_sigma_sigma = []

for i in range(0, len(arr)):
    sum_sigma_sigma.append(sum([x**2 for x in arr[i:]]))

#d
di = [205.2587719,204.9385965, 206.7019348, 200.1243591, 206.7019348, 206.7019348, 206.7019348, 206.7019348, 206.7019348,206.7732067]
#randomforest
# di = [196.9403852,197.2959011, 196.9403852, 197.0707121, 196.2467106, 196.2467106, 196.6193343, 196.6193343, 196.8606222]

p = 120

# 生成服从不同对数分布的numpy数组
c = np.empty(10)
for i in range(10):
    c[i] = (i+1)**2+i+1
c = pd.DataFrame(c.reshape(1,-1))

a = np.empty(10)
for i in range(10):
    a[i] = 50 * (i+2)*np.log(i+2)
a = pd.DataFrame(a.reshape(1,-1))

'''theta1'''
theta1_prior = df['theta1']
std_theta1 = (std_theta + std_epsilon[0] ** 2)**0.5

theta1_posterior = di[0]

z1 = (p - c[0].values)/p

rv = stats.norm(loc=0, scale=1)

pdf1 = rv.pdf(z1)
cdf1 = rv.cdf(z1)

u1 = pdf1 - z1 * (1 - cdf1)

trans1 = z1 * (sum_sigma_sigma[0]) ** 0.5
trans11 = (p-c[0].values) * theta1_prior
trans111 = p * trans1 * u1

Q1 = theta1_prior + trans1
W1 = trans11 - trans111 - a[0].values


'''theta2'''
theta2_prior = df['theta2']
std_theta2 = (std_theta1 ** 2 + std_epsilon[0] ** 2)**0.5

# theta2_posterior
ro2 = sum_sigma_sigma[1]/(std_theta1 ** 2 + std_epsilon[0] ** 2 + sum_sigma_sigma[1])

std_sigma2_posterior = (ro2 * (std_epsilon[0] ** 2 + std_theta1 ** 2)) ** 0.5
theta2_posterior = ro2 * theta2_prior + (1 - ro2) * di[1]

z2 = (p - c[1].values)/p

rv = stats.norm(loc=0, scale=1)

pdf2 = rv.pdf(z2)
cdf2 = rv.cdf(z2)

u2 = pdf2 - z2 * (1 - cdf2)

trans2 = z2*(std_theta1 ** 2 + sum_sigma_sigma[1]) ** 0.5
trans22 = (p-c[1].values) * theta2_posterior
trans222 = p * trans2 * u2

Q2 = theta2_posterior + trans2
W2 = trans22 - trans222 - a[1].values

'''theta3'''

theta3_prior = df['theta3']
std_theta3 = (std_theta2 ** 2 + std_epsilon[1] ** 2)**0.5

# theta2_posterior
ro3 = sum_sigma_sigma[2]/(std_theta2 ** 2 + std_epsilon[1] ** 2 + sum_sigma_sigma[2])

std_sigma3_posterior = (ro3 * (std_epsilon[1] ** 2 + std_theta2 ** 2)) ** 0.5
theta3_posterior = ro3 * theta3_prior + (1 - ro3) * di[2]

z3 = (p - c[2].values)/p

# 生成一个标准正态分布的随机变量
rv = stats.norm(loc=0, scale=1)

# 计算概率密度函数（PDF）
pdf3 = rv.pdf(z3)
# 计算累积分布函数（CDF）
cdf3 = rv.cdf(z3)

u3 = pdf3-z3*(1 - cdf3)

trans3 = z3 * (std_theta2 ** 2 + sum_sigma_sigma[3]) ** 0.5
trans33 = (p-c[2].values) * theta3_posterior
trans333 = p * trans3 * u3

Q3 = theta3_posterior + trans3
W3 = trans33 - trans333 - a[2].values

'''theta4'''
theta4_prior = df['theta4']
std_theta4 = (std_theta3 ** 2 + std_epsilon[2] ** 2)**0.5

# theta2_posterior
ro4 = sum_sigma_sigma[3]/(std_theta3 ** 2 + std_epsilon[2] ** 2 + sum_sigma_sigma[3])

std_sigma4_posterior = (ro4 * (std_epsilon[2] ** 2 + std_theta3 ** 2)) ** 0.5
theta4_posterior = ro4 * theta4_prior + (1 - ro4) * di[3]

z4 = (p - c[3].values)/p

# 生成一个标准正态分布的随机变量
rv = stats.norm(loc=0, scale=1)

# 计算概率密度函数（PDF）
pdf4 = rv.pdf(z4)
# 计算累积分布函数（CDF）
cdf4 = rv.cdf(z4)

u4 = pdf4-z4 * (1 - cdf4)

trans4 = z4 * (std_theta3 ** 2 + sum_sigma_sigma[3]) ** 0.5
trans44 = (p-c[3].values) * theta4_posterior
trans444 = p * trans4 * u4

Q4 = theta4_posterior + trans4
W4 = trans44 - trans444 - a[3].values

'''theta5'''
theta5_prior = df['theta5']
std_theta5 = (std_theta4 ** 2 + std_epsilon[3] ** 2)**0.5

# theta5_posterior
ro5 = sum_sigma_sigma[4]/(std_theta4 ** 2 + std_epsilon[3] ** 2 + sum_sigma_sigma[4])

std_sigma5_posterior = (ro4 * (std_epsilon[3] ** 2 + std_theta4 ** 2)) ** 0.5
theta5_posterior = ro5 * theta5_prior + (1 - ro5) * di[4]

z5 = (p - c[4].values)/p

# 生成一个标准正态分布的随机变量
rv = stats.norm(loc=0, scale=1)

# 计算概率密度函数（PDF）
pdf5 = rv.pdf(z5)
# 计算累积分布函数（CDF）
cdf5 = rv.cdf(z5)

u5 = pdf5-z5 * (1 - cdf5)

trans5 = z5 * (std_theta4 ** 2 + sum_sigma_sigma[4]) ** 0.5
trans55 = (p-c[4].values) * theta5_posterior
trans555 = p * trans5 * u5

Q5 = theta5_posterior + trans5
W5 = trans55 - trans555 - a[4].values

'''theta6'''
theta6_prior = df['theta6']
std_theta6 = (std_theta5 ** 2 + std_epsilon[4] ** 2)**0.5

# theta6_posterior
ro6 = sum_sigma_sigma[5]/(std_theta5 ** 2 + std_epsilon[4] ** 2 + sum_sigma_sigma[5])

std_sigma6_posterior = (ro6 * (std_epsilon[4] ** 2 + std_theta5 ** 2)) ** 0.5
theta6_posterior = ro6 * theta6_prior + (1 - ro6) * di[5]


z6 = (p - c[5].values)/p

# 生成一个标准正态分布的随机变量
rv = stats.norm(loc=0, scale=1)

# 计算概率密度函数（PDF）
pdf6 = rv.pdf(z6)
# 计算累积分布函数（CDF）
cdf6 = rv.cdf(z6)

u6 = pdf6 - z6 * (1 - cdf6)

trans6 = z6 * (std_theta5 ** 2 + sum_sigma_sigma[5]) ** 0.5
trans66 = (p-c[5].values) * theta6_posterior
trans666 = p * trans6 * u6

Q6 = theta6_posterior + trans6
W6 = trans66 - trans666 - a[5].values

'''theta7'''
theta7_prior = df['theta7']
std_theta7 = (std_theta6 ** 2 + std_epsilon[5] ** 2)**0.5

# theta7_posterior
ro7 = sum_sigma_sigma[6]/(std_theta6 ** 2 + std_epsilon[5] ** 2 + sum_sigma_sigma[6])

std_sigma7_posterior = (ro7 * (std_epsilon[5] ** 2 + std_theta6 ** 2)) ** 0.5
theta7_posterior = ro7 * theta7_prior + (1 - ro7) * di[6]

z7 = (p - c[6].values)/p

# 生成一个标准正态分布的随机变量
rv = stats.norm(loc=0, scale=1)

# 计算概率密度函数（PDF）
pdf7 = rv.pdf(z7)
# 计算累积分布函数（CDF）
cdf7 = rv.cdf(z7)

u7 = pdf7 - z7 * (1 - cdf7)

trans7 = z7 * (std_theta6 ** 2 + sum_sigma_sigma[6]) ** 0.5
trans77 = (p-c[6].values) * theta7_posterior
trans777 = p * trans7 * u7

Q7 = theta7_posterior + trans7
W7 = trans77 - trans777 - a[6].values

'''theta8'''
theta8_prior = df['theta8']
std_theta8 = (std_theta7 ** 2 + std_epsilon[6] ** 2)**0.5

# theta8_posterior
ro8 = sum_sigma_sigma[7]/(std_theta7 ** 2 + std_epsilon[6] ** 2 + sum_sigma_sigma[7])

std_sigma8_posterior = (ro8 * (std_epsilon[6] ** 2 + std_theta7 ** 2)) ** 0.5
theta8_posterior = ro8 * theta8_prior + (1 - ro8) * di[7]

z8 = (p - c[7].values)/p

# 生成一个标准正态分布的随机变量
rv = stats.norm(loc=0, scale=1)

# 计算概率密度函数（PDF）
pdf8 = rv.pdf(z8)
# 计算累积分布函数（CDF）
cdf8 = rv.cdf(z8)

u8 = pdf8 - z8 * (1 - cdf8)

trans8 = z8 * (std_theta7 ** 2 + sum_sigma_sigma[7]) ** 0.5
trans88 = (p-c[7].values) * theta8_posterior
trans888 = p * trans8 * u8

Q8 = theta8_posterior + trans8
W8 = trans88 - trans888 - a[7].values

'''theta9'''
theta9_prior = df['theta9']
std_theta9 = (std_theta8 ** 2 + std_epsilon[7] ** 2)**0.5

# theta9_posterior
ro9 = sum_sigma_sigma[8]/(std_theta8 ** 2 + std_epsilon[7] ** 2 + sum_sigma_sigma[8])

std_sigma9_posterior = (ro9 * (std_epsilon[7] ** 2 + std_theta8 ** 2)) ** 0.5
theta9_posterior = ro9 * theta9_prior + (1 - ro9) * di[8]

z9 = (p - c[8].values)/p

# 生成一个标准正态分布的随机变量
rv = stats.norm(loc=0, scale=1)

# 计算概率密度函数（PDF）
pdf9 = rv.pdf(z9)
# 计算累积分布函数（CDF）
cdf9 = rv.cdf(z9)

u9 = pdf9 - z9 * (1 - cdf9)

trans9 = z9 * (std_theta8 ** 2 + sum_sigma_sigma[8]) ** 0.5
trans99 = (p-c[8].values) * theta9_posterior
trans999 = p * trans9 * u9

Q9 = theta9_posterior + trans9
W9 = trans99 - trans999 - a[8].values

# '''theta10'''
# # theta10
# theta10_prior = df['sales']
# std_theta10 = (std_theta9 ** 2 + std_epsilon[8] ** 2)**0.5
#
# # theta10_posterior
# ro10 = sum_sigma_sigma[8]/(std_theta9 ** 2 + std_epsilon[8] ** 2 + sum_sigma_sigma[8])
#
# std_sigma10_posterior = (ro9 * (std_epsilon[8] ** 2 + std_theta9 ** 2)) ** 0.5
# theta10_posterior = ro10 * theta10_prior + (1 - ro10) * di[9]
#
# z10 = (p - c[9])/p
#
# # 生成一个标准正态分布的随机变量
# rv = stats.norm(loc=0, scale=1)
#
# # 计算概率密度函数（PDF）
# pdf10 = rv.pdf(z10)
# # 计算累积分布函数（CDF）
# cdf10 = rv.cdf(z10)
#
# u10 = pdf10 - z10 * (1 - cdf10)
#
# trans10 = (std_theta9 ** 2 + sum_sigma_sigma[8]) ** 0.5
# trans100 = (p-c[9].values) * theta10_posterior
# trans1000 = p * trans10 * (u10.values)
#
# Q10 = theta10_posterior + trans10
# W10 = trans100 - trans1000 - a[9].values

# 假设theta1_posterior, theta2_posterior, ..., std_sigma8_posterior是已知的列表或数组
Q = [Q1, Q2, Q3, Q4, Q5, Q6, Q7, Q8, Q9]
W = [W1, W2, W3, W4, W5, W6, W7, W8, W9]

name = ['theta1','theta2','theta3','theta4','theta5','theta6','theta7','theta8', 'theta9']

Q=pd.DataFrame(index=name,data=Q)
Q=Q.T
Q.to_csv('Qp=120.csv')

W=pd.DataFrame(index=name,data=W)
W=W.T
W.to_csv('Wp=120.csv')
print(c)
print(a)
print(Q)
print(W)
