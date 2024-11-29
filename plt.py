import matplotlib.pyplot as plt
import matplotlib as mpl

font_name = "Microsoft YaHei"
mpl.rcParams['font.family']=font_name
'''
time3 = pd.read_csv("timecost/time3.csv",encoding='gbk')
time5 = pd.read_csv("timecost/time5.csv",encoding='gbk')
time7 = pd.read_csv("timecost/time7.csv",encoding='gbk')
time9 = pd.read_csv("timecost/time9.csv",encoding='gbk')
'''


table = []
row3 = [8.873099985,7.422800001,16.32599998,0.042599975131452084,1.801500039,3.228899965,0.040399958]
row5 = [23.84959999,25.7843,49.76319999,0.060699996538460255,2.945999964,4.212600004,0.049399969]
row7 = [38.069100002758205,47.416699992027134,85.75289999134839,0.11699995957314968,3.0699000344611704,7.044699974358082,0.08029997115954757]
row9 = [61.96039996575564,76.79600000847131,138.9257999835536,0.2269999822601676,3.8388000102713704,7.492100005038083,0.1582999830134213]

table.append(row3)
table.append(row5)
table.append(row7)
table.append(row9)


table_t = list(map(list,zip(*table)))
for row in table_t:
    print(row)
col = [3,5,7,9]
labels = ["生成密钥分片用时","验证密钥分片用时","总体用时","恢复密钥用时","提取公钥用时","单一密钥分片恢复用时","密钥重分享用时"]
for i, y in enumerate(table_t):
    plt.figure()  # 创建新的图形
    plt.bar(col, y, tick_label=col)
    plt.xlabel('参与者人数')
    plt.ylabel('耗时 (ms)')
    plt.title(labels[i])
    plt.savefig(labels[i] + '.png')  # 保存图形为png文件
    plt.close()  # 关闭图形以便下一次绘制