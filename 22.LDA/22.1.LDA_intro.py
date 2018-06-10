# !/usr/bin/python
# -*- coding:utf-8 -*-

from gensim import corpora, models, similarities #使用gensim
from pprint import pprint
#使用的LDA_test文档中，认为一行是一个文档；

# import logging
# logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


if __name__ == '__main__':
    f = open('LDA_test.txt')
    stop_list = set('for a of the and to in'.split())#自己写的停止词，用空格分开，放在set中
    # texts = [line.strip().split() for line in f]
    # print 'Before'
    # pprint(texts)
    print 'After'
    texts = [[word for word in line.strip().lower().split() if word not in stop_list] for line in f]
        #每一个line是一个文档，line.strip()扔掉前后的空格符，转为小写，再根据空格分开，形成一个list，再取出每一个word，只要这个词没在停止词中，就保留下来；
    print 'Text = '
    pprint(texts) #print与pretty print都可以

    dictionary = corpora.Dictionary(texts)#对于这个corpora，把处理好的语料喂进来，得到dictionary；形成文档中不同的、非停止词形成字典
    print dictionary
    V = len(dictionary)#词个数
    corpus = [dictionary.doc2bow(text) for text in texts]#根据词典变为0、1向量
    corpus_tfidf = models.TfidfModel(corpus)[corpus] #统计出这个词在该文档中出现次数，除以在全部文档中出现次数，得tf-idf；
    # corpus_tfidf = corpus#这句没有意义，是这个词在该文档中出现次数

    print 'TF-IDF:'
    for c in corpus_tfidf:
        print c

    print '\nLSI Model:'
    lsi = models.LsiModel(corpus_tfidf, num_topics=2, id2word=dictionary) #用LSI，这个corpus_tfidf可以改为corpus，直接传如出现次数也可以；主题是2个
    topic_result = [a for a in lsi[corpus_tfidf]]#lsi[corpus_tfidf]这部分是可以得到的主题模型
    pprint(topic_result) #输出词是什么
    #LSI中，可能会得到负的相似度，但是逻辑上是不通的，有时为了保证它非负，需要作NFM非负矩阵分解来保证非负；LDA中没有
    print 'LSI Topics:'
    pprint(lsi.print_topics(num_topics=2, num_words=5))#打印两个主题的前5个词
    similarity = similarities.MatrixSimilarity(lsi[corpus_tfidf])   # similarities.Similarity()利用主题分布求相似度
    print 'Similarity:'
    pprint(list(similarity))

    print '\nLDA Model:'
    num_topics = 2
    lda = models.LdaModel(corpus_tfidf, num_topics=num_topics, id2word=dictionary,
                          alpha='auto', eta='auto', minimum_probability=0.001, passes=10)#alpha是主题的超参数，eta是词的超参数；
        #minimum_probability表示当概率小于多少就认为是0，passes语料运行多少次，如果=1，是只做一次，在线学习；
        #minimum_probability表示当概率小于多少就认为是0，截距；
    doc_topic = [doc_t for doc_t in lda[corpus_tfidf]]#得到文档的主题，这个结果一定是非负的，因为是概率，不是矩阵分解
    print 'Document-Topic:\n'
    pprint(doc_topic)
    for doc_topic in lda.get_document_topics(corpus_tfidf):#打印文档的主题分布
        print doc_topic
    for topic_id in range(num_topics):
        print 'Topic', topic_id
        # pprint(lda.get_topic_terms(topicid=topic_id))
        pprint(lda.show_topic(topic_id))
    similarity = similarities.MatrixSimilarity(lda[corpus_tfidf])#求相似度
    print 'Similarity:'
    pprint(list(similarity))

    hda = models.HdpModel(corpus_tfidf, id2word=dictionary) #LDA的结构化处理，如softmax的结构化处理
    topic_result = [a for a in hda[corpus_tfidf]]
    print '\n\nUSE WITH CARE--\nHDA Model:'
    pprint(topic_result)
    print 'HDA Topics:'
    print hda.print_topics(num_topics=2, num_words=5)
