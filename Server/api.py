import copy
import datetime
import time

from Config.settings import config
from Core.spider import Waiter
from threading import Thread
class Global(object):

    def __init__(self):
        self.waiter = None
        self.login = None
        self.thread= None

    def update(self):
        self.login = self.waiter.qrlogin.is_login

glo = Global()

def log(request):
    file_path = config.path() + config.settings("Logger", "FILE_PATH") + \
        config.settings("Logger", "FILE_NAME")
    file_page_file = open(file_path, 'r', encoding="utf-8")
    return str(file_page_file.read())


def serverConfig(request):
    appConfig = copy.deepcopy(config._config._sections)
    for model in appConfig:
        for item in appConfig[model]:
            appConfig[model][item] = eval(appConfig[model][item])
            value = appConfig[model][item]
            # DEBUG print(model, item, value, type(value))
    return appConfig

def get_time_stamp(result):
    utct_date1 = datetime.datetime.strptime(result, "%Y-%m-%dT%H:%M:%S.%f%z")#2020-12-01 03:21:57.330000+00:00
    utct_date2 = time.strptime(result, "%Y-%m-%dT%H:%M:%S.%f%z")#time.struct_time(tm_year=2020, tm_mon=12, tm_mday=1, tm_hour=3, tm_min=21, tm_sec=57, tm_wday=1, tm_yday=336, tm_isdst=-1)
    local_date = utct_date1 + datetime.timedelta(hours=8)#加上时区
    local_date_srt = datetime.datetime.strftime(local_date,"%Y-%m-%d %H:%M:%S.%f")#2020-12-01 11:21:57.330000
    return local_date_srt
    # print('local_date_srt:'+str(local_date_srt))
    # time_array1 = time.mktime(time.strptime(local_date_srt,"%Y-%m-%d %H:%M:%S.%f"))#1606792917.0
    # time_array2 = int(time.mktime(utct_date2))#1606764117
    # print('time_array1:'+str(time_array1))
    # print('time_array2:'+str(time_array2))

def jdShopper(request):
    mode = request['mode']
    date = request['date']
    skuids = request['skuid']
    area = request['area']
    eid = request['eid']
    fp = request['fp']
    count = request['count']
    retry = request['retry']
    work_count = request['work_count']
    timeout = request['timeout']
    print(date)
    if mode == '1':
        print("有货自动下单")
        glo.waiter = Waiter(skuids=skuids, area=area, eid=eid, fp=fp, count=count,
                    retry=retry, work_count=work_count, timeout=timeout)
        glo.thread = Thread(target=glo.waiter.waitForSell)
        glo.thread.start()
    elif mode == '2':
        print('定时下单')
        # date = date.replace("T", " ")
        # date = date.replace("Z", "")
        date = get_time_stamp(date)
        glo.waiter = Waiter(skuids=skuids, area=area, eid=eid, fp=fp, count=count,
                    retry=retry, work_count=work_count, timeout=timeout, date=date)
        glo.thread = Thread(target=glo.waiter.waitTimeForSell)
        glo.thread.start()
    glo.update()
    print(glo.login)
    return glo.login

def loginStatus(request):
    try:
        glo.update()
    except:
        pass
    return glo.login
