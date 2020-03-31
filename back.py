'''
@Author: Javfa
@Date: 2020-03-10 09:24:43
@LastEditors: Javfa
@LastEditTime: 2020-03-30 23:37:07
@FilePath: /projects/techTransfer/outline/back.py
'''
#!/usr/bin/python
# pip install requests
import requests
import time
import hashlib
import json
import re
from fastapi import FastAPI
from pydantic import BaseModel
# import hanlp
from snownlp import SnowNLP

from computeSim import computeSim

app = FastAPI()

# tokenizer = hanlp.load('PKU_NAME_MERGED_SIX_MONTHS_CONVSEG')

class Data(BaseModel):
  input: str

@app.post('/companyInfo')
def companyInfo(dataCompany: Data):
  msg = dataCompany.input
  #  请求参数
  appkey = "6b465d7831bf4b67a5d883092537801a"
  seckey = "043B9DB4552BB652AF66920C705B7C67"
  encode = 'utf-8'

  # Http请求头设置
  timespan = str(int(time.time()))
  token = appkey + timespan + seckey;
  hl = hashlib.md5()
  hl.update(token.encode(encoding=encode))
  token = hl.hexdigest().upper();
  print('MD5加密后为 ：' + token)

  #设置请求Url-请自行设置Url
  reqInterNme = "http://api.qichacha.com/ECIV4/GetFullDetailsByName"
  paramStr = "keyword=" + msg
  url = reqInterNme + "?key=" + appkey + "&" + paramStr;
  headers={'Token': token,'Timespan':timespan}
  response = requests.get(url, headers=headers)

  #结果返回处理
  print(response.status_code)
  resultJson = json.dumps(str(response.content, encoding = encode))
  # convert unicode to chinese
  resultJson = resultJson.encode(encode).decode("unicode-escape")
  print(resultJson)
  industry = re.findall(r'\"Industry\":{.*?}', resultJson)
  products = re.findall(r'\"CompanyProducts\":.*?]', resultJson)
  scope = re.findall(r'\"Scope\":.*?,', resultJson)
  industry = re.findall(r'\"Industry\":(.*)', industry[0])
  industry = json.loads(industry[0])
  # industry = re.findall(r'\"MiddleCategory\":\"([^"]+)', industry[0])
  scope = re.findall(r'\"Scope\":\"([^"]+)', scope[0])
  products = re.findall(r'\"Tags\":\"([^"]+)', products[0])

  company = {}
  if industry != []:
    company['行业分类'] = industry
  if scope != []:
    company['经营范围'] = scope[0]
  if products != []:
    company['产品'] = products[0]

  return company

@app.post('/tok')
def split_cn(data_zh: Data):
  msg = data_zh.input
  # rlt = tokenizer(msg)
  rlt = SnowNLP(msg).words
  return {'success': True, 'rlt': rlt}
  
@app.post('/match')
def match(dataCompany: Data):
  # msg = dataCompany.input
  # #  请求参数
  # appkey = "6b465d7831bf4b67a5d883092537801a"
  # seckey = "043B9DB4552BB652AF66920C705B7C67"
  # encode = 'utf-8'

  # # Http请求头设置
  # timespan = str(int(time.time()))
  # token = appkey + timespan + seckey;
  # hl = hashlib.md5()
  # hl.update(token.encode(encoding=encode))
  # token = hl.hexdigest().upper();
  # print('MD5加密后为 ：' + token)

  # #设置请求Url-请自行设置Url
  # reqInterNme = "http://api.qichacha.com/ECIV4/GetFullDetailsByName"
  # paramStr = "keyword=" + msg
  # url = reqInterNme + "?key=" + appkey + "&" + paramStr;
  # headers={'Token': token,'Timespan':timespan}
  # response = requests.get(url, headers=headers)

  # #结果返回处理
  # print(response.status_code)
  # resultJson = json.dumps(str(response.content, encoding = encode))
  # # convert unicode to chinese
  # resultJson = resultJson.encode(encode).decode("unicode-escape")
  # print(resultJson)
  # industry = re.findall(r'\"Industry\":{.*?}', resultJson)
  # products = re.findall(r'\"CompanyProducts\":.*?]', resultJson)
  # scope = re.findall(r'\"Scope\":.*?,', resultJson)
  # industry = re.findall(r'\"Industry\":(.*)', industry[0])
  # industry = json.loads(industry[0])
  # # industry = re.findall(r'\"MiddleCategory\":\"([^"]+)', industry[0])
  # scope = re.findall(r'\"Scope\":\"([^"]+)', scope[0])
  # products = re.findall(r'\"Tags\":\"([^"]+)', products[0])

  # company = {}
  # if industry != []:
  #   company['行业分类'] = industry
  # if scope != []:
  #   company['经营范围'] = scope[0]
  # if products != []:
  #   company['产品'] = products[0]
  
  return computeSim()
  

  