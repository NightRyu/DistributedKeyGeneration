from PedersenVSS import *
import numpy as np
import gmpy2
import user

rp = gmpy2.random_state()
class p_recover:
    # threhold是门限数，k是需要恢复分享服务器的id
    def __init__(self, threshold, k, num_of_participants):
        self.k = k
        # 生成恢复多项式r1、r2 有r(k)=0
        self.r1 = [gmpy2.mpz_random(rp, q) for _ in range(threshold + 1)]
        self.r1 -= gmpy2.mpz(sum(a * k ** i for i, a in enumerate(self.f1)))
        self.r2 = [gmpy2.mpz_random(rp, q) for _ in range(threshold + 1)]
        self.r2 -= gmpy2.mpz(sum(a * k ** i for i, a in enumerate(self.f1)))
        # 用于盲化的份额
        self.bs = []
        p_commit = []
        f_commit = []
        for a, b in zip(self.r1, self.r2):
            p_value = gmpy2.mod(gmpy2.mul(gmpy2.powmod(g, a, p), gmpy2.powmod(h, b, p)), p)
            f_value = gmpy2.powmod(g, a, p)
            p_commit.append(p_value)
            f_commit.append(f_value)
        # r(0)无意义
        for i in range(num_of_participants + 1):
            # s1 = gmpy2.mod(sum(a * i ** k for k, a in enumerate(self.f1)), q)
            # s2 = gmpy2.mod(sum(b * i ** k for k, b in enumerate(self.f2)), q)
            s1 = gmpy2.mpz(sum(a * i ** k for k, a in enumerate(self.f1)))
            s2 = gmpy2.mpz(sum(b * i ** k for k, b in enumerate(self.f2)))
            value = [i, s1, s2, p_commit, f_commit]
            self.bs.append(value)

    # 使用盲化后份额(P + R)恢复出的多项式是(P + R)()这样(P+R)(k)的值为原多项式的份额
    # TODO:对获取的stocks的验证
    def recover_share(self, stocks):
        x = []
        y = []
        for stock in stocks:
            x.append(stock[0])
            y.append(stock[1])
        poly = lagrange_interpolation(x, y)
        r_stock = poly(self.k)
        return r_stock



'''
class rebuild:
    def __init__(self, old_users, new_users):
        self.old_users = old_users
        # 收集份额恢复原多项式Q
        stocks = []
        for user in old_users:
            stocks.append(user.my_key_stock)
        self.old_q = recover_poly(stocks)
        self.new_users = new_users
'''


def reshare(old_user, new_user):

    return