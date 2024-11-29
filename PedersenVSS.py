import gmpy2
from lagrange import lagrange_interpolation


# 指定的大素数及生成元
p = gmpy2.mpz(0xE3DDAD0C629B3925F455542EF74C6B7A251ADF57BE63400D7762DE24014DE43C6C49DA672EFD6388B7491F5C8017824838C4A457E94E554F4C34316FFC990ABF54E6E5497348C5938968B1D888365E87614EDC25D7FB619C48551A0D5A46F1FFB0BE2BBCEAB3A860B15EE92BE7824C0E7F812FF8B473AA437C9F7E2E90E93E3B)
# q = (p-1) / 2
q = gmpy2.mpz(0x71eed686314d9c92fa2aaa177ba635bd128d6fabdf31a006bbb16f1200a6f21e3624ed33977eb1c45ba48fae400bc1241c62522bf4a72aa7a61a18b7fe4c855faa7372a4b9a462c9c4b458ec441b2f43b0a76e12ebfdb0ce242a8d06ad2378ffd85f15de7559d43058af7495f3c126073fc097fc5a39d521be4fbf1748749f1d)
# 大素数的一个本原根 我选择的这个本原根是素数
g = gmpy2.mpz(0x54e6e5497348c5938968b1d888365e87614edc25d7fb619c48551a0d5a46f1ffb0be2bbceab3a860b15ee92be7824c0e7f812ff8b473aa437c9f7e2e90e9f903)
# g生成子群Z*q中的一个元素，保证log_g h难以计算 要求计算h=g^x mod q x与q互素
h = gmpy2.mpz(0xba7eb5c13b3c2906213efcb9d47a8f3bb88067aca577c9d80b04a1fb65abaa566d5ddf00ca6fecfc045093dab0a5772bd51b19a5cfbe51672931053b0880fdb6e6d0148110ded9279f182a2c4d5a878ee0f767000707a98cfb7eb1602a54489509183222634079f5d2623629ea7139315a6f1dabe1a4a3540a61ec48293f161e)

# p = 23
# q = 11
# g = 5
# h = 8
rp = gmpy2.random_state()
class PedersenVSS:
    def __init__(self, num_of_participants, threshold):
        # 生成多项式
        self.f1 = [gmpy2.mpz_random(rp, q) for _ in range(threshold)]
        self.f2 = [gmpy2.mpz_random(rp, q) for _ in range(threshold)]
        self.ss = []
        # 计算承诺
        self.p_commit = []
        self.f_commit = []
        for a, b in zip(self.f1, self.f2):
            p_value = gmpy2.mod(gmpy2.mul(gmpy2.powmod(g, a, p), gmpy2.powmod(h, b, p)), p)
            f_value = gmpy2.powmod(g, a, p)
            self.p_commit.append(p_value)
            self.f_commit.append(f_value)
        # 计算f1(j),f2(j)，并以[f1(j),f2(j)]的形式存储进ss
        # f(0)是自身的秘密
        for i in range(num_of_participants + 1):
            s1 = gmpy2.mpz(sum(a * i ** k for k, a in enumerate(self.f1)))
            s2 = gmpy2.mpz(sum(b * i ** k for k, b in enumerate(self.f2)))
            value = [i, s1, s2, self.p_commit, self.f_commit]
            self.ss.append(value)


def complaint_feldman(stocks):
    secret = secret_recovery(stocks)
    return gmpy2.powmod(g, secret, p)


def secret_recovery(stocks):
    x = []
    y = []
    for stock in stocks:
        x.append(stock[0])
        y.append(stock[1])
    # 进行拉格朗日插值lagrange_interpolation
    poly = lagrange_interpolation(x, y)
    # 通过计算x = 0处的值恢复秘密
    secret = poly(0, p)
    return secret


def verification_pedersen(stock):
    j, s1, s2, p_commit, f_commit = stock
    lhs = gmpy2.mod(gmpy2.powmod(g, s1, p) * gmpy2.powmod(h, s2, p), p)
    rhs = 1
    for k,val in enumerate(p_commit):
        t = j ** k
        rhs *= gmpy2.powmod(val, t, p)
        rhs = gmpy2.mod(rhs, p)
    return lhs == rhs


def verfication_feldman(stock):
    j, s1, s2, p_commit, f_commit = stock[0]
    lhs = gmpy2.powmod(g, s1, p)
    rhs = 1
    for k,val in enumerate(f_commit):
        rhs *= gmpy2.powmod(val, j ** k, p)
    rhs = gmpy2.mod(rhs, p)
    return lhs == rhs