import fitbit
import numpy as np
import requests
import json
import datetime
import csv

#
# Information: fitbit API have limit 150 per hour.
# RefURL: https://community.fitbit.com/t5/Web-API-Development/Too-many-request/td-p/1644362
#
# Other Ref URL:
#           https://qiita.com/fujit33/items/27d3f3142cf02bb46436
#           https://python-fitbit.readthedocs.io/en/latest/
#           https://dev.fitbit.com/build/reference/web-api/heart-rate/


# Auth param
# client_id     : OAuth 2.0 Client ID (https://dev.fitbit.com/apps)
# client_secret : Client Secret (https://dev.fitbit.com/apps)
# access_token  : you enter the command "python-fitbit/gather_keys_oauth2.py [arg1] [arg2]"
#                   [arg1] : client_id
#                   [arg2] : client_secret
# refresh_token : same the access_token
client_id =  "22D85M"
client_secret  = "bec58326526e7e1bcb921dccf6a36ff6"
access_token =  "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI2VjIyS1QiLCJhdWQiOiIyMkQ4NU0iLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyc29jIHJhY3QgcnNldCBybG9jIHJ3ZWkgcmhyIHJwcm8gcm51dCByc2xlIiwiZXhwIjoxNTM4ODE1MzI3LCJpYXQiOjE1Mzg3ODY1Mjd9.QpFQekisjqpfYOdsT5gD0HJshyw5oh7zZTTlCG8agGE"
refresh_token =  "ae66d97ab25c3e7d851d87b66a32605cad4a2910a3242d1dbb71ea5bc531a46e"

#出力はカレントディレクトリに日付を付与したファイル名でファイルを作成
output_file = datetime.datetime.now().strftime("%Y%m%d_%H%M") + "_fitbit.txt"



#
# return : date strings array
# param
#   start_year: start day of "year"
#   start_month: start day of "month"
#   start_day: start day of "day"
#   days: period from baseline to the future
#
def create_date_string(start_year=2018,start_month=10,start_day=1,days=1):
    cal = []
    loop = np.arange(0,days,1)

    calc_source = datetime.datetime(start_year, start_month, start_day, 0, 00, 00)

    for i in loop:
      d = int(i)
      str1 = str(calc_source + datetime.timedelta(days=d))
      str1 = str1.split(" ")
      cal.append(str1[0])

    return cal


# 取得したい日付
#DATE = "2018-10-01"の形式で指定日数分取得
# create_date_string(2018,9,1,50)の場合は2018-09-01から2018-10-20までの文字列配列を生成
DATE = create_date_string(2018,9,1,50)

# ID等の設定
authd_client = fitbit.Fitbit(client_id, client_secret
                             ,access_token=access_token, refresh_token=refresh_token)
authd_client.sleep()

#出力用配列準備
write_header = ['date,heart']

#データ取得
num = np.arange(0,len(DATE),1)
for i in num:
    # 心拍数を取得（1秒単位）
    data_sec_array = authd_client.intraday_time_series('activities/heart', DATE[i], detail_level='1min') #'1sec', '1min', or '15min'

    #データ数が1以上の時だけデータ抽出、書き出しを実施する
    data_size = len(data_sec_array["activities-heart-intraday"]["dataset"])
    if data_size > 0 :
        #時分秒 + 心拍数の形でデータが取得される
        data_sec_array = data_sec_array["activities-heart-intraday"]["dataset"]

        #データ抽出＆データ形式変換
        date_str_array = [ DATE[i] + " " + str(data_sec["time"]) for data_sec in data_sec_array]
        heart_str_array = [str(data_sec["value"]) for data_sec in data_sec_array]

        #ファイルへ書き出し
        with open(output_file,'a') as f:
            writer = csv.writer(f,lineterminator='\n')
            writer.writerow(write_header)
            for (date_str,heart_str) in zip(date_str_array,heart_str_array):
                writer.writerow([date_str,heart_str])
