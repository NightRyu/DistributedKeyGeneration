from PedersenVSS import *
import numpy as np
import gmpy2
import user

rp = gmpy2.random_state()
class recover:
    # threhold是门限数，k是需要恢复分享服务器的id
    def __init__(self, threshold, k, num_of_participants):
        self.k = k
        # 生成恢复多项式r1、r2 有r(k)=0
        self.r = [gmpy2.mpz_random(rp, q) for _ in range(threshold + 1)]
        self.r[0] -= gmpy2.mpz(sum(a * k ** i for i, a in enumerate(self.r)))
        # 用于盲化的份额 r(0)无意义
        self.bs = []
        for i in range(num_of_participants + 1):
            # s1 = gmpy2.mod(sum(a * i ** k for k, a in enumerate(self.f1)), q)
            # s2 = gmpy2.mod(sum(b * i ** k for k, b in enumerate(self.f2)), q)
            s = gmpy2.mpz(sum(a * i ** k for k, a in enumerate(self.r)))
            value = [i, s]
            self.bs.append(value)

    # 使用盲化后份额(P + R)恢复出的多项式是(P + R)()这样(P+R)(k)的值为恢复出的份额，且不会暴露原多项式的值
    def recover_share(self, stocks):
        x = []
        y = []
        for stock in stocks:
            x.append(stock[0])
            y.append(stock[1])
        poly1 = lagrange_interpolation(x, y)
        r_stock = poly1(self.k, p)
        return r_stock


class reshare:
    def __init__(self, old_users, new_users, threshold):
        self.old_users = old_users
        # 生成随机多项式Q、Q'，用于盲化份额，进行秘密传递
        # 两个多项式用于Pederesen VSS承诺及验证
        self.old_q = [gmpy2.mpz_random(rp, q) for _ in range(threshold)]
        self.new_users = new_users
        self.new_q = [gmpy2.mpz_random(rp, q) for _ in range(threshold)]
        # 二者常数项相等
        self.new_q[0] = 5
        self.old_q[0] = 5
        self.bs = []


    def get_blind_stock(self):
        for i,o_user in enumerate(self.old_users):
            stock = []
            stock.append(o_user.user_id)
            # 计算Q(k)的值
            v_old = gmpy2.mpz(sum(a * o_user.user_id ** k for k, a in enumerate(self.old_q)))
            # 盲化原用户的分享
            v_old += o_user.my_key_stock[1]
            stock.append(v_old)
            self.bs.append(stock)


    def share_new(self):
        for n_user, stock in zip(self.new_users, self.bs):
            n_user.user_id = stock[0]
            v = gmpy2.mpz(sum(a * n_user.user_id ** k for k, a in enumerate(self.new_q)))
            n_user.my_key_stock = [n_user.user_id, stock[1] - v]