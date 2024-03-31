import gmpy2


def primitive_root(modulo):
    k = (modulo - 1) // 2
    count = 0
    for i in range(0xaa7372a4b9a462c9c4b458ec441b2f43b0a76e12ebfdb0ce242a8d06ad2378ffd85f15de7559d43058af7495f3c126073fc097fc5a39d521be4fbf1748749f1d, modulo - 1):
        if gmpy2.powmod(i, k, modulo) != 1:
            count += 1
            if gmpy2.is_prime(i):
                print(hex(i))
        if count == 50000:
            break


rs = gmpy2.random_state()
def subgroup(p,g):
    x = gmpy2.mpz_random(rs, p)
    print(hex(x))
    h = gmpy2.powmod(g, x, p)
    return h


def root_of(q, h):
    k = (q - 1) // 2
    if gmpy2.powmod(h, k, q) != 1:
        return True
    else:
        return False



q = gmpy2.mpz(0x71eed686314d9c92fa2aaa177ba635bd128d6fabdf31a006bbb16f1200a6f21e3624ed33977eb1c45ba48fae400bc1241c62522bf4a72aa7a61a18b7fe4c855faa7372a4b9a462c9c4b458ec441b2f43b0a76e12ebfdb0ce242a8d06ad2378ffd85f15de7559d43058af7495f3c126073fc097fc5a39d521be4fbf1748749f1d)
# primitive_root(q)
g = gmpy2.mpz(0x54e6e5497348c5938968b1d888365e87614edc25d7fb619c48551a0d5a46f1ffb0be2bbceab3a860b15ee92be7824c0e7f812ff8b473aa437c9f7e2e90e9f903)
# h = subgroup(q, g)
# print(hex(h))
h = gmpy2.mpz(0xba7eb5c13b3c2906213efcb9d47a8f3bb88067aca577c9d80b04a1fb65abaa566d5ddf00ca6fecfc045093dab0a5772bd51b19a5cfbe51672931053b0880fdb6e6d0148110ded9279f182a2c4d5a878ee0f767000707a98cfb7eb1602a54489509183222634079f5d2623629ea7139315a6f1dabe1a4a3540a61ec48293f161e)
# print(root_of(q,h))