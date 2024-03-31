import gmpy2


def lagrange_interpolation(x, y):
    # 定义插值函数
    def _poly(x_val, p):
        total = gmpy2.mpz(0)
        n = len(x)
        for i in range(n):
            xi, yi = x[i], y[i]
            # 定义g函数，用于计算拉格朗日插值的每一项
            def g(i, n):
                tot_mul = gmpy2.mpz(1)
                for j in range(n):
                    if i == j:
                        continue
                    xj, yj = x[j], y[j]
                    # 计算每一项的值
                    tot_mul *= (x_val - xj) / (xi - xj)
                return gmpy2.mpz(tot_mul)
            # 计算插值函数的值
            total += yi * g(i, n)
            total = gmpy2.mod(total, p)
        return gmpy2.mod(total, p)
    return _poly