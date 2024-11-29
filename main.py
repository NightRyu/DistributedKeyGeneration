from copy import copy
import COBRA
import user
import gmpy2
import PedersenVSS
import time
import csv #调用数据保存文件
import pandas as pd #用于数据输出


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print("Please enter the number of participants.")
    participants = int(input())
    print("Please enter the number of threshold.")
    threshold = int(input())
    parties = []

    cost = []
    time_recoder = []
    init_times = []  # 生成密钥分片用时
    veri_times = []  # 验证密钥分片用时
    total_times = []  # 总体用时
    getx_times = []  # 恢复密钥用时
    gety_times = []  # 提取公钥用时
    recover_times = []  # 单一密钥分片恢复用时
    reshare_times = []  # 密钥重分享用时
    start_time = time.perf_counter()
    print(start_time)
    for i in range(participants):
        part = user.User(i ,participants, threshold)
        parties.append(part)
    fin_init = time.perf_counter()
    # print("fin_init", fin_init - start_time)
    init_times = (fin_init - start_time)*1000

    for part in parties:
        part.distribute_keys(parties)

    for part in parties:
        part.verfication()
        part.get_new_stock(parties)
    fin_veri = time.perf_counter()

    # 任意一个用户均可以检查并将用户踢出QUAL
    for part in parties:
        part.check_QUAL(parties)

    for part in parties:
        part.get_my_stock()
    fin_genx = time.perf_counter()
    print("Total cost", fin_genx - start_time)
    total_times = (fin_genx - start_time)*1000

    parties[0].collect_stock(parties)
    x = parties[0].recovery_secret()
    print("生成的密钥为",hex(x))
    fin_getx = time.perf_counter()
    # print("Get key", fin_getx - fin_genx)
    getx_times = (fin_getx - fin_genx)*1000

    # 测试最终密钥是否是各方秘密和
    y = parties[0].extract_y(parties)
    print("提取出的公钥为",hex(y))
    fin_ext = time.perf_counter()
    # print("Extract Y", fin_ext - fin_getx)
    gety_times = (fin_ext - fin_getx)*1000

    temp = copy(parties[1].my_key_stock)
    print("参与者1的分片为",hex(temp[1]))
    parties[1].recover_share(parties)
    print("恢复参与者1的分片为",hex(parties[1].my_key_stock[1]))
    fin_recover = time.perf_counter()
    # print("Recover share", fin_recover - fin_ext)
    recover_times = (fin_recover - fin_ext)*1000

    new_parties = []
    for i in range(participants):
        n_part = user.User(i ,participants, threshold)
        new_parties.append(n_part)

    st_reshare = time.perf_counter()
    rs = COBRA.reshare(parties, new_parties, threshold)
    rs.get_blind_stock()
    rs.share_new()
    n_stocks = []
    for n_part in new_parties:
        n_stocks.append(n_part.my_key_stock)
    print("重分享后恢复出的密钥为",hex(PedersenVSS.secret_recovery(n_stocks)))
    fin_reshare = time.perf_counter()
    # print("Reshare cost",fin_reshare - st_reshare)
    reshare_times = (fin_reshare - st_reshare)*1000
'''
    time_recoder.append(init_times)
    time_recoder.append(veri_times)
    time_recoder.append(total_times)
    time_recoder.append(getx_times)
    time_recoder.append(gety_times)
    time_recoder.append(recover_times)
    time_recoder.append(reshare_times)
    cost.append(time_recoder)

    colume = ["生成密钥分片用时","验证密钥分片用时","总体用时","恢复密钥用时","提取公钥用时","单一密钥分片恢复用时","密钥重分享用时"]
    times = pd.DataFrame(columns = colume, data = cost)
    times.to_csv("time9.csv")
'''