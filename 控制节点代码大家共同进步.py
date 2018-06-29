# -*- coding: utf-8 -*-
import requests
from flask import Flask,request,jsonify
import datetime
import time
#opc
import OpenOPC

app = Flask(__name__)  # 实例化app对象

#冷冻机组控制
@app.route('/ldj/write', methods=['GET'])  # 路由
def opc_write():
    opc = OpenOPC.client()  #创建客户端
    opc.connect(u'PCAuto.OPCServer', 'localhost')  #读取opc
    pointName=request.values["pointName"]      #获取坐取按钮信息
    pointValue=request.values["pointValue"]
    opc.write((str(pointName), float(pointValue)))  #写入opc值
    time.sleep(1)
    lista = ["ZLJ2_ManOn.PV", "ZLJ2_Run.PV", "ZLJ2_ManAuto.PV", "ZLJ3_ManOn.PV", "ZLJ3_Run.PV", "ZLJ3_ManAuto.PV"]#控制集
    listStatus = []
    opcList = opc.read(lista) #读取整个流程参数 0停止和手动  1启动和自动
    for line in opcList:
        collection = {}
        collection[line[0]] = line[1]
        listStatus.append(collection)
    return jsonify(listStatus)   #f返回状态结果集

#冷冻机组控制结果查询
@app.route('/ldj/status', methods=['GET'])  # 路由
def opc_status():
    opc = OpenOPC.client()  #创建客户端
    opc.connect(u'PCAuto.OPCServer', 'localhost')  #读取opcserver
    lista = ["ZLJ2_ManOn.PV", "ZLJ2_Run.PV", "ZLJ2_ManAuto.PV", "ZLJ3_ManOn.PV", "ZLJ3_Run.PV", "ZLJ3_ManAuto.PV"]
    listStatus = []
    opcList = opc.read(lista) #读取整个流程参数 0停止和手动  1启动和自动
    for line in opcList:
        collection = {}
        collection[line[0]] = line[1]
        listStatus.append(collection)
    return jsonify(listStatus)   #f返回状态结果集

# 风机盘管组控制
@ app.route('/pg/write', methods=['GET'])  # 路由
def pg_write():
    pointX = request.values["pointX"]   #坐标点
    pointY = request.values["pointY"]
    result=requests.post("http://10.65.244.162:5000/imageBack",data={'x':pointX,'y':pointY})#下发命令
    return jsonify(result.status_code)  #返回200及成功


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=7777, debug=True)
