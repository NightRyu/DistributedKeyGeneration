from copy import copy
import user
import gmpy2
import PedersenVSS


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print("Please enter the number of participants.")
    participants = int(input())
    print("Please enter the number of threshold.")
    threshold = int(input())
    parties = []
    for i in range(1, participants + 1):
        part = user.User(i ,participants, threshold)
        parties.append(part)

    for part in parties:
        part.distribute_keys(parties)

    for part in parties:
        part.verfication()
        part.get_new_stock(parties)

    # 任意一个用户均可以检查并将用户踢出QUAL
    for part in parties:
        part.check_QUAL(parties)

    for part in parties:
        part.get_my_stock()

    parties[0].collect_stock(parties)
    x = parties[0].recovery_secret()
    print(hex(x))
    print(hex(gmpy2.powmod(PedersenVSS.g, x, PedersenVSS.p)))

    # 测试最终密钥是否是各方秘密和
    y = parties[0].extract_y()
    print(hex(y))
    print(y == gmpy2.powmod(PedersenVSS.g, x, PedersenVSS.p))

    temp = copy(parties[0].my_key_stock)
    parties[0].recover_share(parties)
    print(temp[1] == parties[0].my_key_stock[1])
    '''
    yy = 1
    for part in parties:
        yy *= part.pvss.ss[0][4][0]
        yy = gmpy2.mod(yy, PedersenVSS.p)
    print(hex(yy))
    '''
    '''
    # 直接提取秘密验证生成是否正确，实验用
    xx = 0
    for part in parties:
        xx += part.pvss.ss[0][1]
        xx = gmpy2.mod(xx, PedersenVSS.p)
    print(hex(xx))
    print(xx == x)
    '''