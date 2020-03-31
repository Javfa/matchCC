'''
@Author: Javfa
@Date: 2020-03-10 08:45:03
@LastEditors: Javfa
@LastEditTime: 2020-03-30 23:34:18
@FilePath: /projects/techTransfer/outline/front.py
'''
import streamlit as st
import requests

html_tmp = """
    <div style="background-color:tomato;padding:10px">
    <h2 style="color:white;text-align:center;">企业和成果匹配查询系统</h2>
    </div>
    """
st.markdown(html_tmp, unsafe_allow_html=True)

st.markdown('---')

option = st.selectbox('请选择你想要使用的功能：',
                      ('', '分词', '查询公司信息', '匹配成果'))
content = st.text_input('请输入公司名称：')

if option == '查询公司信息':

  if st.button('查询公司信息') & (content != ''):
    data_bin = {'input': content}
    rlt = requests.post('http://192.168.199.110:80/companyInfo', json=data_bin).json()
    st.write(rlt)
elif option == '分词':
  if st.button('分词') & (content != ''):
    data_bin = {'input': content}
    rlt = requests.post('http://192.168.199.110:80/tok', json=data_bin).json()
    st.write(rlt)
elif option == '匹配成果':
  if st.button('匹配成果')& (content != ''):
    data_bin = {'input': content}
    rlt = requests.post('http://192.168.199.110:80/match', json=data_bin).json()
    st.write(rlt)
else:
  pass