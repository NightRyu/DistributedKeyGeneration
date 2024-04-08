from PedersenVSS import *
from COBRA import *
import gmpy2


class User:
    def __init__(self, user_id, participants, threshold):
        self.pvss = PedersenVSS(participants, threshold) # 生成要分发的分片和秘密
        self.participants = participants # 参与者数量
        self.threshold = threshold
        self.user_id = user_id
        self.stocks = [] # 收到的秘密分片，[id, s1, s2, p_commit, f_commit]
        self.collected_stocks = [] # 收集其它用户的秘密分片，用于计算自己的秘密
        self.my_key_stock = [] # 对收集到的有效秘密分片求和
        self.qualified_user = [] # 合格参与者的ID
        self.complant_user = [] # 存疑参与者的ID
        self.disqualified_user = [] # 失格参与者的ID


    def distribute_keys(self, users):
        for user in users:
            # 分发与用户ID匹配的份额
            stock = [self.pvss.ss[user.user_id], True]  # 默认份额是正确的，在验证中会修改
            user.stocks.append(stock)


    # 验证被分发的份额是否正确
    def verfication(self):
        count = 1
        for stock in self.stocks:
            stock[-1] = verification_pedersen(stock[0])
            if stock[-1]: # 正确则加入QUAL中
                 self.qualified_user.append(count)
            else: # 不正确则存疑
                self.complant_user.append(count)
            count += 1


    # 请求重复获取份额
    def get_new_stock(self, users):
        for user in users:
            if user.user_id in self.complant_user:
                stock = user.new_stock(self.user_id)
                # 仍不符合要求则失去资格
                if not verification_pedersen(stock):
                    self.disqualified_user.append(user.user_id)
                else:
                    self.qualified_user.append(user.user_id)


    # 检查被complaint的用户是否超过t次，超过则踢出QUAL
    def check_QUAL(self, users):
        for user1 in users:
            num_complaint = 0
            for user2 in users:
                if user1.user_id in user2.complant_user:
                    num_complaint += 1
            if num_complaint > self.threshold or user1.user_id in self.disqualified_user:
                if  user1.user_id in self.qualified_user:
                    self.qualified_user.remove(user1.user_id)


    # 重分配份额，可扩展重计算份额
    def new_stock(self, uid):
        stock = self.pvss.ss[uid]
        return stock


    def get_my_stock(self):
        self.my_key_stock.append(self.user_id)
        self.my_key_stock.append(0)
        self.my_key_stock.append(0)
        for stock in self.stocks:
            if stock[-1]:# 如果stock属于QUAL
                self.my_key_stock[1] += stock[0][1]


    def collect_stock(self, users):
        # 收集份额
        for user in users:
            if user.user_id in self.qualified_user:
                self.collected_stocks.append([user.my_key_stock,True])


    def recovery_secret(self):
        if len(self.qualified_user) >= self.threshold:
            certificated_stocks = []
            for stock in self.collected_stocks:
                if stock[-1]:
                    certificated_stocks.append(stock[0])
            return gmpy2.mod(secret_recovery(certificated_stocks), p)
        else:
            return "No Enough QUAL User"


    def extract_y(self):
        y = 1
        for i, stock in enumerate(self.stocks):
            if i + 1 in self.qualified_user:
                if verfication_feldman(stock):
                    y *= stock[0][4][0]
                    y = gmpy2.mod(y, p)
                else:
                    # 恢复其秘密
                    stock_piece = []
                    for user in self.qualified_user:
                        # 从每个QUAL用户中获取未验证通过用户的密钥分片
                        stock_piece.append(user.stocks[stock[0] - 1])
                    # 恢复zi的值，并再次运算g^zi mod p
                    y *= complaint_feldman(stock_piece)
        y = gmpy2.mod(y, p)
        return y


    def recover_share(self, users):
        rec = p_recover(self.threshold, self.user_id, self.participants)
        b_stocks = []
        for user in users:
            bs = [rec.bs[user.user_id], True]
            b_stocks.append(user.blinded_share(bs))
        self.my_key_stock = rec.recover_share(b_stocks)

    def blinded_share(self, bs):
        if verification_pedersen(bs):
            b_stock = self.my_key_stock
            b_stock[1] += bs[1]
            b_stock[2] += bs[2]
            return b_stock
        else:
            return False