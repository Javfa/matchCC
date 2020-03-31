'''
@Author: Javfa
@Date: 2020-03-30 22:59:54
@LastEditors: Javfa
@LastEditTime: 2020-03-30 23:14:46
@FilePath: /projects/techTransfer/outline/computeSim.py
'''

import numpy as np
import scipy
from scipy.spatial import distance
import mysql.connector
from snownlp import SnowNLP
import re

from paddlehub.reader.tokenization import load_vocab
import paddle.fluid as fluid
import paddlehub as hub


def convert_tokens_to_ids(vocab, text):
    wids = []
    tokens = text.split(" ")
    for token in tokens:
        wid = vocab.get(token, None)
        if not wid:
            wid = vocab["unknown"]
        wids.append(wid)
    return wids


def computeSim():

    module = hub.Module(name="word2vec_skipgram")
    inputs, outputs, program = module.context(trainable=False)
    vocab = load_vocab(module.get_vocab_path())

    word_ids = inputs["word_ids"]
    embedding = outputs["word_embs"]

    place = fluid.CPUPlace()
    exe = fluid.Executor(place)
    feeder = fluid.DataFeeder(feed_list=[word_ids], place=place)

    mydb = mysql.connector.connect(host='58.213.198.77', port = '10068', user='root', passwd='Ttxs0315!', database='techTransfer')
    mycursor = mydb.cursor()
    sql = "select * from cn_lib_cat_4th"
    mycursor.execute(sql)
    result = mycursor.fetchall()
    originalRes = result
    result = [i[1] for i in result] # 取得中图分类文字部分
    result = [re.sub(r'[^\w]', '', i) for i in result] # 删除标点符号
    result = [SnowNLP(i).words for i in result if i != ''] # 分词
    result = [' '.join(i) for i in result] # 用空格连接成字符串

    data = [['开发 设计 生产 销售 移动 通信 系统 手机', i] for i in result]

    sims = [[] for i in range(len(data))]
    
    for i, item in enumerate(data):
        text_a = convert_tokens_to_ids(vocab, item[0])
        text_b = convert_tokens_to_ids(vocab, item[1])

        vecs_a, = exe.run(
            program,
            feed=feeder.feed([[text_a]]),
            fetch_list=[embedding.name],
            return_numpy=False)
        vecs_a = np.array(vecs_a)
        vecs_b, = exe.run(
            program,
            feed=feeder.feed([[text_b]]),
            fetch_list=[embedding.name],
            return_numpy=False)
        vecs_b = np.array(vecs_b)

        sent_emb_a = np.sum(vecs_a, axis=0)
        sent_emb_b = np.sum(vecs_b, axis=0)
        cos_sim = 1 - distance.cosine(sent_emb_a, sent_emb_b)

        sims[i].append(item[0])
        sims[i].append(item[1])
        sims[i].append(cos_sim)
    

    sims = sorted(sims, key=lambda item: item[2], reverse=True)

    cat = ''.join(sims[0][1].split(' '))

    for i in range(len(originalRes)):
      if originalRes[i][1] == cat:
        print(originalRes[i][0])

    #print(sims)
    sql = "select title from collegeAchievements where cnLibraryCategory like 'TN91%' limit 1000"
    mycursor.execute(sql)
    result = mycursor.fetchall()
    print(result)
    return result


if __name__ == "__main__":
    computeSim()