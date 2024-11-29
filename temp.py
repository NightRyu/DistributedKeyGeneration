from lagrange import lagrange_interpolation
from gmpy2 import *
import numpy as np

x = [0,1,2,3,4,5,6,7,8,9]
cofs = [[mpz(8), mpz(1), mpz(3), mpz(7), mpz(8), mpz(10)],
[mpz(7), mpz(8), mpz(5), mpz(2), mpz(3), mpz(6)],
[mpz(3), mpz(7), mpz(6), mpz(9), mpz(6), mpz(2)],
[mpz(5), mpz(6), mpz(3), mpz(5), mpz(7), mpz(7)],
[mpz(3), mpz(1), mpz(8), mpz(9), mpz(1), mpz(10)],
[mpz(4), mpz(0), mpz(9), mpz(8), mpz(3), mpz(7)],
[mpz(2), mpz(1), mpz(7), mpz(5), mpz(6), mpz(7)],
[mpz(4), mpz(2), mpz(6), mpz(1), mpz(1), mpz(4)],
[mpz(4), mpz(10), mpz(8), mpz(4), mpz(2), mpz(7)]]

ys = []
i = 0
for cof in cofs:
    s1 = sum(a * i ** k for k, a in enumerate(cof))


polys = []
for y in ys:
    poly = lagrange_interpolation(x,y)
    polys.append(poly)

# 各个多项式插值恢复的和
yyy = 0
for poly in polys:
    yyy += poly(0, 9999)
print(yyy)

# 共同决定的多项式
yy = []
n = len(y)
for i in range(n):
    col = [row[i] for row in ys]
    yy.append(sum(col))
print(yy)

# 直接插值恢复
p = lagrange_interpolation(x, yy)
print(p(0, 9999))