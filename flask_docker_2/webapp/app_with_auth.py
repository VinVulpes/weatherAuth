from flask import Flask,request  
from datetime import date
import os, requests, re, grpc,  message_pb2, message_pb2_grpc

app = Flask(__name__)

#key = '5dad5ab210114bbf98e141921231902'
key = '1db4fdaea7d8457dbd5220318232402'
WEATHER_API_VAR = os.getenv('WEATHER_API')
def checkAuth():
    try:
        user_name = request.headers['Own-Auth-UserName']
    except KeyError:
        return 'Bad request, the User-Name header is missing', 400
    with grpc.insecure_channel("auth:9000") as channel: #'localhost:9000' если на машине
            # stub = message_pb2_grpc.AuthServiceStub(channel)
            # response = stub.CheckAuthorization(message_pb2.AuthRequest(user_name=request.headers["Own-Auth-UserName"]))
            stub = message_pb2_grpc.AuthServiceStub(channel=channel)
            response = stub.CheckAuthorization(message_pb2.AuthRequest(user_name=user_name))
            if response.is_authorized:
                return 'Ok', 200
    return 'Authentication failed', 403
@app.route('/')
def home():
    return '<h1>Домашная работа №2 Вместе с сервером авторизации</h1><h3>Получение прогноза - /forecast</h3><h3>Получение текущей погоды - /current</h3>'
@app.route('/forecast/city=<city>&dt=<dt>')
def forecast(city,dt):
    auth = checkAuth()
    if auth[1] !=200:
        return auth
    today = date.today()
    re_dt= dt.split('-')
    re_dt[1] = re.sub(r'0\d', re_dt[1][1], re_dt[1])
    re_dt[2] = re.sub(r'0\d', re_dt[2][1], re_dt[1])
    diff = (date(int(re_dt[0]),int(re_dt[1]),int(re_dt[2])) - today).days
    #between 14 and 365 days from the current day
    if diff >13 and diff<366:
        space = 'future'
    # less 14 days
    else:
        space = 'forecast'    
   #if date.today() date.
    data = requests.get(WEATHER_API_VAR+space+'.json?key='+key+'&q='+city+'&dt='+dt).text
    country = re.search(r'"country":"[a-zA-Z -]*",',data).group(0)
    city_req = '"city":"'+re.search(r'(?<="name":")[a-zA-Z -]*",',data).group(0)
    avgtemp_c = '"avg_temp":'+re.search(r'(?<="avgtemp_c":)-?\d*.?\d*',data).group(0)+','
    mintemp_c = '"min_temp":'+re.search(r'(?<="mintemp_c":)-?\d*.?\d*',data).group(0)+','
    maxtemp_c = '"max_temp":'+re.search(r'(?<="maxtemp_c":)-?\d*.?\d*',data).group(0)
    res = '{'+country+city_req+avgtemp_c+mintemp_c+maxtemp_c+'}'
    return eval(res)
@app.route('/current/city=<city>')
def current(city):
    auth = checkAuth()
    if auth[1] !=200:
        return auth
    data = requests.get(WEATHER_API_VAR+'current.json?key='+key+'&q='+city).text
    country = re.search(r'"country":"[a-zA-Z -]*",',data).group(0)
    city_req = '"city":"'+re.search(r'(?<="name":")[a-zA-Z -]*",',data).group(0)
    temp_c = '"temp_c":'+re.search(r'(?<="temp_c":)-?\d*.?\d*',data).group(0)+','
    res = '{'+country+city_req+temp_c+'}'
    return eval(res)
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)