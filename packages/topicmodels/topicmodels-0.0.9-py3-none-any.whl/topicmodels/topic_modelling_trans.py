import keras
from tensorflow.keras.callbacks import LambdaCallback
import eval_measure
from corpus import DocData,DocDatalstm
import ldann
from ldann import Doc2Topic,Logger,data_feeder,Doc2Topiclstm
from eval_measure import custom_evaluator
import os
import collections
import numpy as np
import random
import json
import pandas as pd
import fasttext
from scipy import spatial


# wordmodel = fasttext.load_model(modelweights_path)
# fastdict=wordmodel.get_words()
# t5
from transformers import TFAutoModelWithLMHead, AutoTokenizer
model = TFAutoModelWithLMHead.from_pretrained("t5-base")
tokenizer = AutoTokenizer.from_pretrained("t5-base")

def removepad(summarydata):
    finalsummr=[]
    for i in range(len(summarydata)):
        sent=summarydata[i]
        sent=sent.split()
        complt=""
        for j in sent:
            if j=='<pad>':
                continue
            else:
                complt+=j
                complt+=' '
        finalsummr.append(complt)     
    return finalsummr

    
def word_frq(str):
    counts = dict()
    words = str.split()
    for word in words:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1
    tmpsum=""
    for i in counts:
        tmpsum+=i+' '
    return tmpsum


def topicmodelingtransformer(dataset,no_topic,topic_word,column_name='clean_tweet'):
    modelweights_path="C:/Users/SANJEEV/Desktop/complete code 13feb/fasttext10.bin"
    print("starting transformer model")
    num_topic=no_topic
    topic_num=int(num_topic)
    word_num=int(topic_word)
    complete_data=dataset
    print("checking data")
#     print("hello world")
    if(topic_num>len(complete_data)):
        print("insufficient data")
        return
    else:   
        print("reading data")
        rows=len(complete_data)/topic_num
        rows=int(rows)
        combine_rows=[]
        i=0
        while i in range(len(complete_data)):
            tmprow=''
            lnl=min(rows,len(complete_data))
            pred_tmp=complete_data.iloc[i:i+lnl]
            for j in range(len(pred_tmp)):
                tmprow=tmprow+pred_tmp.iloc[j][column_name]
                tmprow+=' '
            combine_rows.append(tmprow)
            i=i+lnl
        newdata=pd.DataFrame({column_name:combine_rows})  
    
    complete_datatrans=newdata
    print("loading summarization model")
    from transformers import TFAutoModelWithLMHead, AutoTokenizer
    model = TFAutoModelWithLMHead.from_pretrained("t5-base")
    tokenizer = AutoTokenizer.from_pretrained("t5-base")
    # t5summary_model_define()
    realtweet=[]
    sumtweet=[]
    single_summr=[]
    print("predicting topics")
    for i  in range(len(complete_datatrans)):
        tweetart=complete_datatrans.iloc[i][column_name]
        tweetart=str(tweetart)
        inputs = tokenizer.encode("summarize: " +tweetart, return_tensors="tf", max_length=1400,truncation=True)
        outputs = model.generate(inputs, max_length=word_num, length_penalty=2.0, num_beams=2, early_stopping=True)
        realtweet.append(tweetart)
        outtweet=tokenizer.decode(outputs[0])
        sumtweet.append(outtweet)
        single_summr.append(word_frq(outtweet))
        
    single_summr=removepad(single_summr)
    total=pd.DataFrame({'real':realtweet,'pred':sumtweet,'non_repeat_summr':single_summr})
    total=total.iloc[0:min(len(total),topic_num)]
    print("loading fasttext model")
    wordmodel = fasttext.load_model(modelweights_path)
    fastdict=wordmodel.get_words()
    finalscore=0
    finaltopics=[]
    print("calculating score")
    for i in range(len(total)):
        tmptopic=total.iloc[i]['non_repeat_summr']
        crttopic=tmptopic.split()
        tmptopic=''
        for j in range(len(crttopic)):
            tmptopic+=crttopic[j]
            if j<(len(crttopic)-1):
                tmptopic+=' ,'
        finaltopics.append(tmptopic)
        if len(crttopic)<2:
            continue
        else:
            v=crttopic[0]
            v=wordmodel[v]
            tmpscore=0
            for j in range(1,len(crttopic)):
                spcword=crttopic[j]
                u=wordmodel[spcword]
                crscore=result = 1 - spatial.distance.cosine(u,v)
                tmpscore=tmpscore+crscore
            if(tmpscore)>0:
                finalscore+=tmpscore
    print("score calcution done")
    finalscore/=len(total)
    finaltopics=pd.DataFrame({'topic':finaltopics})
    return finaltopics,finalscore
    
