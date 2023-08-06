from ....util.config import SurfingConfigurator
from ...api.basic import BasicDataApi
from ....util.wechat_bot import *

MAX_SIZE = 25

class DataChecker:

    def __init__(self):
        self.wechat_bot = WechatBot()
        self.wechat_hook = SurfingConfigurator().get_wechat_webhook_settings('wechat_webhook_data_check')

    def process_index_price(self):
        try:
            key_index_list = ['sse50','hs300','csi500','gem','star50','sp500rmb','national_debt','mmf']
            index_info = BasicDataApi().get_index_info(index_list=key_index_list)
            index_price = BasicDataApi().get_index_price(index_list=index_info.index_id.tolist())
            index_price = index_price.pivot_table(index='datetime',values='close',columns='index_id')
            desc_dic = index_info.set_index('index_id')['desc_name'].to_dict()
            last_date = index_price.index[-1]

            res = []
            for index_id in index_price:
                index_name = desc_dic[index_id]
                start_date = index_price[index_id].dropna().index[0]
                end_date = index_price[index_id].dropna().index[-1]
                if end_date == last_date:
                    s = f'    {index_id} {index_name} {start_date} {end_date} \r'
                else:
                    s = f'    异常 {index_id} {index_name} {start_date} {end_date} \r'
                res.append(s)

            bucket_size = int(len(res) / MAX_SIZE) + 1
            for i in range(bucket_size):
                idx_b = i * MAX_SIZE
                idx_e = min((i + 1) * MAX_SIZE - 1, len(s))
                _res = f'[常用指数数据更新情况] part {i+1} 上一个交易日日期 {last_date}\r'
                for r in res[idx_b:idx_e]:
                    _res += r
                message = {
                    'msgtype': 'markdown',
                    'markdown': {
                        'content': _res
                    }
                }
                res = requests.post(url=self.wechat_hook, data=json.dumps(message), timeout=20)

        except Exception as e:
                print(f'Failed to get data <err_msg> {e} from DataChecker.process_index_price')

    def process_fund_nav(self):
        try:
            # todo
            check_num = 1000
            fund_info = BasicDataApi().get_fund_info()
            fund_info = fund_info.head(check_num)
            fund_list = fund_info.fund_id.tolist()
            fund_open_info = BasicDataApi().get_fund_open_info()
            fund_open_list = fund_open_info.fund_id.tolist()

            fund_nav = BasicDataApi().get_fund_nav(fund_list)
            fund_nav  = fund_nav.pivot_table(index='datetime', columns='fund_id', values='adjusted_net_value')

            default_end_date = datetime.date(2040,12,31)
            last_date = fund_nav.index[-1]
            last_friday = (last_date
                - datetime.timedelta(days=last_date.weekday())
                + datetime.timedelta(days=4, weeks=-1))
            qdii_last_date = last_date - datetime.timedelta(days=1)

            res = []
            for r in fund_info.itertuples():
                info_end_date = r.end_date
                if r.fund_id not in fund_nav:
                    continue
                    
                end_date = fund_nav[r.fund_id].dropna().index[-1]
                # 定开
                if r.fund_id in fund_open_list:
                    
                    if end_date >= last_friday:
                        continue
                    else:
                        dic = {
                            'fund_id':r.fund_id,
                            'desc_name':r.desc_name,
                            'wind_class_2':r.wind_class_2,
                            'type':f'定开基金 缺少最新净值 最后净值日 {end_date}'
                        }
                        res.append(dic)
                        continue
                # qdii
                if r.wind_class_2 in ['国际(QDII)股票型基金','国际(QDII)债券型基金']:
                    if end_date >= qdii_last_date:
                        continue
                    else:
                        dic = {
                            'fund_id':r.fund_id,
                            'desc_name':r.desc_name,
                            'wind_class_2':r.wind_class_2,
                            'type':f'qdii基金 缺少最新净值 最后净值日 {end_date}'
                        }
                        res.append(dic)
                        continue
                
                # 非终止基金    
                if info_end_date == default_end_date:
                    if end_date == last_date:
                        continue
                    else:
                        dic = {
                            'fund_id':r.fund_id,
                            'desc_name':r.desc_name,
                            'wind_class_2':r.wind_class_2,
                            'type':f'基金未终止 缺少最新净值 最后净值日 {end_date}'
                        }
                        res.append(dic)
                        continue
                # 终止基金
                else:
                    if (info_end_date - end_date).days > 7:
                        dic = {
                            'fund_id':r.fund_id,
                            'desc_name':r.desc_name,
                            'wind_class_2':r.wind_class_2,
                            'type':f'基金已终止 缺少净值 终止日 {info_end_date} 最后净值日 {end_date}'
                        }
                        res.append(dic)
                        continue
                    else:
                        continue
                
            df = pd.DataFrame(res)
            bucket_size = int(df.shape[0] / MAX_SIZE) + 1
            for i in range(bucket_size):
                idx_b = i * MAX_SIZE
                idx_e = min((i + 1) * MAX_SIZE - 1, df.shape[0])
                res = f'[基金数据] part {i+1} 上一个交易日日期 {last_date}\r'
                for r in df.loc[idx_b:idx_e].itertuples():
                    s = f'    {r.fund_id} {r.desc_name} {r.wind_class_2} {r.type} \r'
                    res += s
                message = {
                    'msgtype': 'markdown',
                    'markdown': {
                        'content': res
                    }
                }
                res = requests.post(url=self.wechat_hook, data=json.dumps(message), timeout=20)

        except Exception as e:
                print(f'Failed to get data <err_msg> {e} from DataChecker.process_fund_nav')

    def process(self):
        self.process_fund_nav()
        self.process_index_price()


