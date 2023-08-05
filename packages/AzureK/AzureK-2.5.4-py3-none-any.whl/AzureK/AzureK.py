# -*- coding: utf-8 -*-

'''
**AzureK_datahelp**
=====

**模块说明**
-----------------------------
**由AzureK编写的函数模块，里面存放了本人在数据处理过程中经常用到的一些函数，用于对常见的重复性工作进行一些简化，以提升处理效率.**\n

导入方式及建议缩写
    >>> import AzureK as dh
    >>> from AzureK import AzureK as dh(pip install则采用这个)
'''
import json
import urllib.parse
import time
import urllib3
import urllib
import os
import pandas as pd
import numpy as np
from scipy.optimize import leastsq
import statsmodels.api as sm
import dateutil
import datetime

def version():
    print('目前版本:2.5')
    return None

def changelog():
    '''
    **版本2.5更新日志**
    -----------------------------
    1.CAR功能完善, 新增date_postpone,为True可以自动顺延至该企业首个交易日进行CAR计算\n
    2.CAR参数简化,删除了package可选项,现在只能选择statsmodels,删除output选项,仅输出一个result结果\n
    3.删除colloc_change函数\n
    4.优化了部分函数的参数名,不影响后续使用\n
    
    **版本2.4更新日志**
    -----------------------------
    1.新增函数CSMAR_read_excel函数,消除国泰安原始表格中的首行英文列名和第三行的单位名\n    
    
    **版本2.3更新日志**
    -----------------------------
    1.修改了CAR算法中在CAR计算区间非对称情况下的CAR计算结果不正确的bug\n
    
    **版本2.2更新日志**
    -----------------------------
    1.新增parse函数,基于dateutil中的parse,先对time做了str,防止timestamp格式的报错\n
    2.CAR的OLS默认计算包改为statemodels\n
    3.read_excel新增collen_fill参数,布尔值,用于是否对股票代码进行位数填补(海外股非数字,不能填补)\n
    4.CAR计算程序中相应的增加了index_collen_fill和stock_collen_fill两个参数,分别对应指数数据和股票数据\n
    5.解决了CAR中事件日期精确到时分秒时候不能和指数\个股\交易日数据匹配的问题\n
    6.修改read_excel函数,将时间列单独设置为一个参数,并和CAR函数做了适配,经过测试可以正常使用\n
    
    
    **版本2.1.2更新日志**
    -----------------------------
    1.重写Module_upgrade函数中的说明\n
    2.优化CAR函数,拟合部分可选两种数据处理库(scipy,statsmodels),经检验,两者结果在小数点后五位前无差别，statsmodels会输出R2和AdjR2的结果\n

    **版本2.1.1更新日志**
    -----------------------------
    1.修复了CAR函数中check_threshold名称错误及其功能不能正常使用的问题
    
    **版本2.1更新日志**
    -----------------------------
    模块内部函数互相局部化,尤其是在for循环内调用的函数,如read_excel
    1.修复了read_excel中的bug
            TypeError: can only concatenate str (not "numpy.int64") to str
    
    **版本2.0更新日志**
    -----------------------------
    2.0版本对所有已有的函数进行了检查和梳理,按顺序介绍如下:
    1.getHtml:
        将decode_format参数更名为decode
    2.getAllFileName:
        how参数修改,新增totalname表示带格式的文件名,原本的file变为不含格式的文件名
    3.replaces:
        新增ignore,白名单,stringlist中是ingore列表中的元素均不会做任何替换
    4.ColumnsUniform:
        dfcol_uniform函数更名
        修复了当被统一化的列名是Uniform列名的子集时候出现的部分替代的问题(如公告发布日期会被替换成公告公发布日期)
        注:词库之间的一一对应关系或许可能通过字典来实现, 日后可能会改进
    5.dfcol_change:
        本函数从完成后再也没有使用过,和模块内其他函数也没有交集,因此目前不做任何处理,直接复制过来
    6.新增new_parse函数:
        在parse函数套了一层try-except避免重复parse的报错
        并且原本的parse不能识别年月日，本函数用replace使其能够识别
    7.read_excel:
        删除了fillna操作和无效的time_col参数
        新增market判断,当函数内有交易所信息时,根据交易所信息选择collen对应的数值
    8.baiduSentiment:
        新增了百度情感分析api函数
        修改了print内容,现在是评论内容+极性
        新增decode参数,默认为GBK,一般来说都是这个格式,但是以防万一
    9.CAR:
        CAR的修改主要是以下几个方面：
        1. 无法进行CAR计算的数据不直接舍弃,会注明无法计算的原因,并可以可选参数output选择是否保留
        2. 支持从同一个文件中读取不同股票的数据或者不同指数的数据
        3. 新增函数CAR_DifferentMarkets支持包含多个交易所的股票的数据表的计算，包括(港股数据和美股数据)
    10.updateTradingData
        本函数直接搬运了，没有做任何的修改，和dfcol_change一样，使用频率过低
        
    **版本1.2.0更新日志**
    -----------------------------
    1.read_excel函数新增sheet_name参数,功能同pd.read_excel(sheet_name).\n
    
    **版本1.1.1更新日志**
    -----------------------------
    1.修改了模块介绍和函数注释的排版,使其更加简洁易读.\n
    2.新增ModuleUpgrade函数,安装方法备忘录,用于查询如何更新本模块.
    
    **版本1.1.0更新日志**
    -----------------------------
    1.重写replaces函数,消除原版本中的bug并更加实用.\n
    2.删除了dfcolumns_uniform函数中标题词库中的'标题'(该问题并没有彻底解决,但是避免了该词导致的bug).\n
    3.新增函数getHtml和getAllFileName.\n
    4.新增changelog函数,用于查询更新日志.\n
    '''
    
def ModuleUpgrade():
    '''
    模块更新方法
    -----------------------------
    (一).pip install AzureK
    (二):将AzureK.py文件复制到anaconda的数据包路径下
    
    附:pypi上模块上传更新方法
        1.cmd打开到模块的setup.py所属路径cd D:\jjk\研究生\程序\AzureK
        2.
    '''
    #C:\Users\flhsjjk\anaconda3\Lib\site-packages

def getHtml(url,decode = ''):
    '''
    函数功能
    -----------------------------
    读取网页代码\n
    
    变量介绍
    -----------------------------
    url:str格式,网页地址\n
    decode_format:str格式,decode格式,常见的有gb2312,ASCII等等\n
    
    返回结果
    -----------------------------
    str格式的网页的完整代码
    '''
    html = urllib.request.urlopen(url)
    info = html.read().decode(decode,errors = 'ignore')
    return info

def getAllFileName(file_dir, how = 'all'):
    '''
    函数功能
    -----------------------------
    读取文件夹中所有的文件\n
    
    变量介绍
    -----------------------------
    file_dir:
        str格式,文件夹路径\n
    how:
        str格式,可选file和all两种,对应输入结果分别是,仅返回文件夹内文件名称,返回文件完整路径,根据个人习惯,默认返回all\n
        
    返回结果
    -----------------------------
    how = totalname 返回filedir路径下的所有文件名所组成的列表,包括了文件格式后缀
    how = all 返回filedir路径下所有文件的完整路径名,即(filedir+file)的列表
    how = file 返回filedir路径下的文件名, 不包括后缀
    '''
    Name_and_form_List = []
    TotalDir_List = []
    for root, dirs, files in os.walk(file_dir):  
        Name_and_form_List.extend(files)
        TotalDir_List.extend(['\\'.join((root,i)) for i in files])
    if how == 'totalname':
        return Name_and_form_List
    elif how == 'file':
        return [i.split('.')[0] for i in Name_and_form_List]
    elif how == 'all':
        return TotalDir_List

def replaces(olds, new, string = '', str_list = [],  how = 'all', ignore = []):
    '''
    函数功能
    -----------------------------
    基于replace函数把string字符串内的符合olds列表内元素的内容依次替换为new的内容\n
    
    变量介绍
    -----------------------------
    string:
        str格式,要进行replace操作的字符串\n
    str_list:
        list格式,要进行所有元素都要进行replace操作的列表，其中每个元素都要是字符串\n
    olds:
        list格式,要替换的内容,列表内每一个元素都是要被替换掉的内容\n
    new:
        list格式或者str格式,要替换成的内容,若是list格式,则必须和olds一一对应,若为str格式,则是将string中的与olds中元素相同部分都替换为new\n
    how:
        str格式,all和any二选一,all表示string或者strlist中元素要经过每一个olds列表中的词汇的替换,any则是如果替换成功一次,就终止替换,不再继续\n
    ignore:
        List,白名单,仅对stringlist有效,stringlist和ingore交集元素将不作替换
        
    返回结果
    -----------------------------
    经过replaces替换后的列表或者字符串
    '''
    def StringReplace(string, olds, new, how):
        '''
        函数功能:对string进行replace
        '''
        if isinstance(new,str):
            if how == 'any':
                for old in olds:
                    NewString = string.replace(old, new)
                    if NewString != string:
                        break
                return NewString
            elif how == 'all':
                NewString = string
                for old in olds:
                    NewString = NewString.replace(old, new)
                return NewString
        elif isinstance(new,list) and len(new)==len(olds):
            if how == 'any':
                for i in range(len(new)):
                    NewString = string.replace(olds[i],new[i])
                    if NewString != string:
                        break
                return NewString
            elif how == 'all':
                NewString = string
                for i in range(len(new)):
                    NewString = NewString.replace(olds[i],new[i])
                return NewString
        else:
            print('how参数或者new类型输入有误')
            return -1
    if string != '':
        return StringReplace(string, olds, new, how)
    elif str_list != []:
        NewStringList = []
        for string in str_list:
            if string not in ignore:
                NewStringList.append(StringReplace(string, olds, new, how))
            else:
                NewStringList.append(string)
        return NewStringList
    else:
        print('string或者stringList输入有误')
        return -1

def ColumnsUniform(dfcol= [], df= None, how = 'any'):
    '''
    函数功能
    -----------------------------
    不同表格的命名存在差异，但是往往几种表示表达的是同一个东西，本函数就是对其统一化处理，规则如下：\n
    1.股票代码: 证券代码=股票代码=公司代码=上市公司代码=code \n
    2.企业简称: 公司简称=企业简称=证券简称=company=company_short_name \n
    3.公告发布日期: 发布时间=公告发布时间=公告发布日期=发布日期=time=date \n
    4.公告标题: 标题内容=公告标题=title \n
    5.公告内容: 公告内容=具体内容=文章内容=content \n
    **词库的元素必须满足一个原则:若一个元素是另一个元素的子集(如发布日期是公告发布日期的子集),子集必须要摆放更靠后的位置**\n
    
    变量介绍
    -----------------------------
    dfcol:
        list格式,dataframe的列名列表 \n
    df:
        pandas.dataframe格式 \n
    how:
        str格式,可以选择any或者all,any对应的算法是一种词库仅使用一次，也就是说一个列表中如果某项被替换了，那么该词库在后续的replace中不会再次使用，all则是无差别全部遍历 \n   
        
    返回结果
    -----------------------------
    输入的是dfcol则会返回处理后的列表格式文件
    输入的是df则会返回列名变换后的df
    '''
    code_Thesaurus = ['证券代码','企业代码','公司代码','上市公司代码','code']  #Thesaurus词库的意思，下同
    company_Thesaurus = ['企业简称', '证券简称', 'company', 'company_short_name']
    time_Thesaurus = ['公告发布时间','发布时间', 'time', 'date']
    title_Thesaurus = ['标题内容', 'title']
    content_Thesaurus = ['公告内容', '文章内容', 'content']
    stock_return_Thesaurus = ['个股回报率']
    Total_Thesaurus = [code_Thesaurus, company_Thesaurus, time_Thesaurus, title_Thesaurus, content_Thesaurus, stock_return_Thesaurus]
    AllElements_in_Thesaurus = []
    [AllElements_in_Thesaurus.extend(x) for x in Total_Thesaurus]
    Uniform = ['股票代码', '企业简称', '公告发布日期', '公告标题', '公告内容','日个股回报率'] #uniform和Total_Thesauru的数量必须保持一致且一一对应关系
    #正常的表格，列名里证券代码的信息只会出现一次，那么只要出现过，后面的列名就不需要再进行匹配了
    def dfcol_uni(dfcol, Total_Thesaurus, Uniform, how, uni_dfcol = []):
        '''
        函数功能:通过母函数设定好的词库以及统一化词汇,对输入的列名列表中的每一个元素进行标准化处理
        uni_dfcol:进过标准化处理之后的dfcol
        '''
        if dfcol == []:
            return uni_dfcol
        elif how == 'any': #递归算法
            col = dfcol[0]
            dfcol = dfcol[1:] #每次都只读取dfcol第一个元素，然后将其从dfcol中除去
            for index in range(len(Total_Thesaurus)):
                origincol = col #origin_col表示原本的col,因为下面比较再进行替换操作后是否出现了变化
                if origincol in Uniform:
                    index = Uniform.index(origincol) #原本列名就是标准化后的格式,对应的词库也就没有存在的必要了
                    uni_dfcol.append(col)
                    Total_Thesaurus = Total_Thesaurus[:index] + Total_Thesaurus[index+1:]
                    Uniform = Uniform[:index] + Uniform[index+1:]
                    break
                elif origincol not in AllElements_in_Thesaurus:
                    uni_dfcol.append(col)
                    break
                thesaurus = Total_Thesaurus[index]
                uniword = Uniform[index]
                col = replaces(olds = thesaurus, new = uniword, string = col , how = 'any')
                if col != origincol:
                    Total_Thesaurus = Total_Thesaurus[:index] + Total_Thesaurus[index+1:] #将已经生效过的词库以及统一后词汇从中剔除
                    Uniform = Uniform[:index] + Uniform[index+1:]
                    uni_dfcol.append(col)
                    break
                elif index == len(Total_Thesaurus)-1:
                    uni_dfcol.append(col)
            return dfcol_uni(dfcol, Total_Thesaurus, Uniform, how, uni_dfcol = uni_dfcol)  #递归循环
        elif how == 'all':
            for col in dfcol:
                if col in Uniform:
                    uni_dfcol.append(col)
                    continue
                elif origincol not in AllElements_in_Thesaurus:
                    uni_dfcol.append(col)
                    continue
                for index in range(len(Total_Thesaurus)):
                    thesaurus = Total_Thesaurus[index]
                    uniword = Uniform[index]
                    col = replaces(thesaurus, uniword, string = col)
                uni_dfcol.append(col)
            return uni_dfcol
        else:
            print('how参数输入有误,仅可为all或any')     
    def df_uni(df): 
        '''
        函数功能:对dataframe格式的列名进行了统一化处理,基本是调用了dfcol_uni函数，只是在此基础上,把统一化后的列名列表重新赋值给了df
        '''
        unidf = df.copy(deep = True) #unidf为统一化后的df,copy中的deep参数为true表示复制后改动df不会影响unidf,若为false则会影响
        dfcol = df.columns.tolist()
        dfcol = [str(i).replace('\'','') for i in dfcol]
        uni_dfcol = dfcol_uni(dfcol, Total_Thesaurus, Uniform, how, uni_dfcol = [])
        unidf.columns = uni_dfcol
        return unidf
    if dfcol != []:
        dfcol = [str(i).replace('\'','') for i in dfcol] #国泰安的数据列名里面可能会带'
        return dfcol_uni(dfcol, Total_Thesaurus, Uniform, how, uni_dfcol = [])
    elif not(df is None):#如果写成df!=None的判断条件,会typeerror,所以通过is以及not进行判断,双重否定表示肯定
        return df_uni(df)
    else:
        print('未输入有效的列名列表或df')
        return -1
    
def read_excel(file_path, collen = 6,  collen_fill = True, code_col = '股票代码', market_col = '', sheet_name = '', str_col = ['指数代码','股票代码','交易日期'], time_col = []):
    '''
    函数功能
    -----------------------------
    根据实际操作中的需要,在read_excel基础上添加功能:对时间和股票代码str化,并保证code的规范性
    
    变量介绍
    -----------------------------
    file_path:
        str格式,读取的文件的完整路径\n
        
    返回结果
    -----------------------------
    按照filepath读取并经过ColumnsUniform统一化处理了列名的df
    '''
    
    '''
    局部化函数
    '''
    local_ColumnsUniform = ColumnsUniform
    
    def CodeCol_Check(df, code_col, collen, market_col):
        '''
        由于历史原因,部分数据集里面的code是int很可能会和其他数据集里的字符串式股票代码冲突,因而再次做统一修正,所有的元素必须是长度为6的str格式
        函数功能:检查代码列对存在问题的股票代码列数据进行格式上的修正
        '''
        def CodeCol_Check_by_Market(df, code_col, market_col):
            market_codelen_dict = {'SH':6, 'SZ':6, 'HK':'5'}
            for index in range(len(df)):
                market = str(df.loc[index,market_col]).upper()
                code = str(df.loc[index, code_col])
                try:
                    df.loc[index, code_col] =  '0'*(market_codelen_dict[market]-len(code)) + df.loc[index, code_col]
                except:
                    continue
                '''
                if market == 'SH' or market == 'SZ':
                    df.loc[index, code_col] = '0'*(6-len(code)) + df.loc[index, code_col]
                elif market == 'HK' :
                    df.loc[index, code_col] = '0'*(5-len(code)) + df.loc[index, code_col]   
                else:
                    continue
                '''
            return df
        if market_col != '':
            df = CodeCol_Check_by_Market(df, code_col, market_col)
        elif isinstance(collen, int) and collen_fill == True:
            df[code_col] = df[code_col].apply(lambda x: '0'*(collen - len(str(x)))+str(x))
            '''
            for index in range(len(df)):
                code = df.loc[index, code_col]
                df.loc[index, code_col] = '0'*(collen - len(str(code))) + df.loc[index, code_col]
            '''
        return df
    str_dict = {}
    for i in str_col:
        str_dict[i] = str
    if sheet_name != '':
        df = local_ColumnsUniform(df = pd.read_excel(file_path, dtype = str_dict, sheet_name = sheet_name))
    else:
        df = local_ColumnsUniform(df = pd.read_excel(file_path, dtype = str_dict))
    if len(time_col) > 0:
        for each_col in time_col:
            df[each_col] = df[each_col].apply(parse)
    return CodeCol_Check(df, code_col, collen, market_col) #返回经过code检查及修改的数据集

def CSMAR_read_excel(read_path,to_excel=True):
    data = pd.read_excel(read_path)
    data.columns = data.loc[0,:].tolist()
    data = data.loc[2:,:].reset_index(drop=True)
    if to_excel == True:
        new_file_path = read_path.replace('.xlsx','_clean.xlsx')
        data.to_excel(new_file_path,index=False)
        return data,new_file_path
    else:
        return data

def baiduSentiment(data, CommentCol = '评论内容', client_id = 'jZgx0XTi08BKfLX0jNpmLea9', client_secret = '3f4AijnG0G59NTXCennNmuvUGZ7qM0Fu',decode = 'GBK'):
    CommentData = data.copy(deep = True)
    values = {
     'host':'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials',
     'client_id': client_id,
     'client_secret' : client_secret 
    }
    def getAccessToken(values):
        host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={}&client_secret={}'.format(values['client_id'],values['client_secret'])
        request = urllib.request.Request(host)
        request.add_header('Content-Type', 'application/json; charset=UTF-8')
        response = urllib.request.urlopen(request)
        content = response.read()
        if (content):
            content = json.loads(content)
            AccessToken = content['access_token']
            return AccessToken
        else:
            print('error!')
            return -1  
    AccessToken = getAccessToken(values)
    url = 'https://aip.baidubce.com/rpc/2.0/nlp/v1/sentiment_classify?access_token={}'.format(AccessToken)
    CommentContentList = [i.split('：',maxsplit=1)[-1] for i in CommentData[CommentCol].tolist()]
    def SentimentResultAppend (positive_prob, confidence, negative_prob, sentiment, SentimentDict = {}):
        if SentimentDict == {}:
            positive_prob.append('')
            confidence.append('')
            negative_prob.append('')
            sentiment.append('')
        elif len(SentimentDict) == 4:
            positive_prob.append(SentimentDict['positive_prob'])
            confidence.append(SentimentDict['confidence'])
            negative_prob.append(SentimentDict['negative_prob'])
            sentiment.append(SentimentDict['sentiment'])
        else:
            print('SentimentDict有误')
            
    http = urllib3.PoolManager()
    positive_prob =[]
    confidence = []
    negative_prob = []
    sentiment = []
    #index = int(input('输入起始点\n>>>'))
    for i in range(len(CommentContentList)):
        if (i+1)%2 == 0:
            time.sleep(1)
        params={'text':CommentContentList[i]}
        #进行json转换的时候，encode编码格式不指定也不会出错
        encoded_data = json.dumps(params).encode(decode)
        request = http.request('POST', 
                              url,
                              body = encoded_data,
                              headers = {'Content-Type':'application/json'})
        #对返回的byte字节进行处理。Python3输出位串，而不是可读的字符串，需要进行转换 
        #注意编码格式
        result = json.loads(str(request.data, decode))
        try:
            SentimentDict = result['items'][0]
            SentimentResultAppend(positive_prob, confidence, negative_prob, sentiment, SentimentDict = SentimentDict)
        except:
            SentimentResultAppend(positive_prob, confidence, negative_prob, sentiment, SentimentDict = {})
        print('内容:', CommentContentList[i][:10],'   极性:',sentiment[i])
    CommentData['情感极性'] = sentiment
    CommentData['积极概率'] = positive_prob
    CommentData['消极概率'] = negative_prob
    CommentData['分类置信度'] = confidence    
    return CommentData

CAR_dict = {'mainland_index': 'd:\\jjk\\研究生\\医药板块上市公司\\上市公司公告\\国泰安数据\\医药指数数据库\\',
            'mainland_stock': 'd:\\jjk\\研究生\\医药板块上市公司\\上市公司公告\\国泰安数据\\医药企业个股收益率数据库\\',
            'mainland_trading': r'd:\jjk\研究生\医药板块上市公司\上市公司公告\国泰安数据\交易日期表.xlsx',
            'SH_index': 'd:\\jjk\\研究生\\医药板块上市公司\\上市公司公告\\国泰安数据\\医药指数数据库\\',
            'SH_stock': 'd:\\jjk\\研究生\\医药板块上市公司\\上市公司公告\\国泰安数据\\医药企业个股收益率数据库\\',
            'SH_trading': r'd:\\jjk\\研究生\医药板块上市公司\上市公司公告\国泰安数据\交易日期表.xlsx',
            'SZ_index': 'd:\\jjk\\研究生\\医药板块上市公司\\上市公司公告\\国泰安数据\\医药指数数据库\\',
            'SZ_stock': 'd:\\jjk\\研究生\\医药板块上市公司\\上市公司公告\\国泰安数据\\医药企业个股收益率数据库\\',
            'SZ_trading': r'd:\jjk\研究生\医药板块上市公司\上市公司公告\国泰安数据\交易日期表.xlsx',
            'HK_index': '',
            'HK_stock': '',
            'HK_trading': ''}

def parse(time):
    '''
    函数功能
    -----------------------------
    日期格式的转换
    
    变量介绍
    -----------------------------
    time:
        str或其他常用的日期格式
    '''
    try:
        return dateutil.parser.parse(str(time))
    except:
        print('时间数据有误')
        return -1

def CAR(df, index_code, estimated_period = [(-128,-8)], windows_period = (-5,5), CAR_interval = [(-5,5),(-4,4),(-3,3),(-2,2),(-1,1),(-1,0),(0,1)], 
        date_title = '公告发布日期', suspension_limit = 0, date_postpone = False, date_postpone_title = '顺延后首个交易日',
        index_data_path = CAR_dict['mainland_index'], stock_data_path = CAR_dict['mainland_stock'], tradingday_data_path = CAR_dict['mainland_trading'], 
        index_col = ['交易日期','指数回报率'], stock_col = ['交易日期','日个股回报率'], tradingday_col = ['交易日期'], 
        market_col = '', stock_collen_fill = True, index_collen_fill = True):
    '''
    函数功能
    -----------------------------
    异常收益率的计算
    
    变量介绍
    -----------------------------
    df:
        dataframe格式,需要进行计算的事件数据集,至少需要包括事件的标题 发布时间以及发布的企业的股票代码三项\n
    stock_data_path:
        str格式,股票日常收益率文件路径,和df公告数据中的股票代码一起组成所需要调取的股票收益率数据文件路径\n
    index_data_path:
        str格式,指数日常收益率文件路径,和index_code一起组成所需要调取的指数数据文件路径\n
    tradingday_data_path:
        str格式,交易日期表文件路径,用于后续确认某企业发布公告时间点上的估计期区间内是否存在停牌\n
    estimated_period:
        list格式,其中所有元素必须是元组tuple,事件估计期,确定用于估计的区间因为估计区间可能包括事前事后两部分,因而需要用元组形式\n
    windows_period:
        list或者tuple格式,事件窗口期,窗口期区间必须是关于0对称的!!\n
    CAR_interval:
        list格式,其中所有元素必须为tuple,用于指明计算CAR的区间范围\n
    date_title:
        str格式,指明dataframe中事件发生时间的那一列
    
    返回结果
    -----------------------------
    在原df基础上新增数列,包括拟合斜率截距和窗口期的每一天以及预设的CAR计算区间
    '''
    
    '''
    局部化函数如下:
    '''
    local_read_excel = read_excel
    
    def slice_list(date, date_list, interval, interval_element):
        '''
        函数功能,根据提供的日期、包含该日期的列表以及需要切片的区间范围,返回切片结果
        date:datetime格式,日期
        date_list:list格式,其每个元素都是datetime格式,需要查询和定位的时间列表
        interval:list格式,其中元素要么全是数字,要么全是元组,元组内也必须全部是数字,元祖或者interval的长度都必须为2
        interval_element:str格式,用于注明interval是什么,数字则注明为int,元祖则注明为tuple
        '''
        if interval_element == 'int':
            index = date_list.index(date)
            start = index + interval[0]
            end = index + interval[1] + 1 #之所以+1是因为list的切片[x:y]是一个左闭右开的区间
            return date_list[start:end]
        elif interval_element == 'tuple':
            index = date_list.index(date)
            slice_list = []
            for i in interval:
                start, end = index + i[0],index + i[1] + 1
                slice_list.extend(date_list[start:end])
            return set(slice_list)
        else:
            print('element选项有误')
            return -1           
    def DateCheck(date, stock_trading_list, tradingday_list, estimated_period, windows_period, suspension_limit):
        '''
        函数功能:CAR必要的估计期内不能有较长时间的停牌,窗口期更是必须全部交易,因而本函数是对是否存在停牌的检查(在非交易日发布的公告直接视为存在停牌)
        date:datetime格式,某企业某项公告的发布日期
        stock_trading_list:list格式,date对应的企业的交易日列表,日期从远至近排序
        '''
        '''先判断个股数据是否足够估计期与窗口期的切片选择'''
        index = stock_trading_list.index(date)
        TimeThreshold = []
        for i in [windows_period]+estimated_period:
            TimeThreshold.extend(list(i))
        TimeMax,TimeMin = max(TimeThreshold),min(TimeThreshold)
        try:
            stock_trading_list[index+TimeMin:index+TimeMax]
        except:
            return '该股票交易数据不全'
        '''再判断窗口期是否存在停牌'''
        if slice_list(date, tradingday_list, windows_period, interval_element = 'int') != slice_list(date, stock_trading_list, windows_period, interval_element = 'int'):
            return '事件窗口期停牌时间超过限制' #窗口期存在任何不同则说明企业有停牌,直接返回false
        '''窗口期无误后,再判断估计期是否存在大量停牌'''
        if len(slice_list(date, tradingday_list, estimated_period, interval_element = 'tuple').intersection(slice_list(date, stock_trading_list, estimated_period, interval_element = 'tuple'))) < len(slice_list(date, tradingday_list, estimated_period, interval_element = 'tuple'))-suspension_limit:
            return '估计期停牌时间超过限制' #窗口期存在任何不同则说明企业有停牌,直接返回false
        else:
            return True
    def ARleastsq(data_x ,data_y):
        '''
        函数功能:最小二乘法拟合
        参考文章:https://blog.csdn.net/weixin_37203756/article/details/80550886
        定义的func和error函数分别对应于拟合曲线格式以及残差
        data_x、data_y:numpy.array格式,分别对应于进行拟合的x数据以及y数据(CAR中,指数收益率是x,个股实际收益率是y)
        '''
        def func(p,x):
            k,b = p
            return k*x+b
        def error(p,x,y):
            return func(p,x)-y
        p0 = np.random.rand(2) #k,b的初始值，可以任意设定
        Para = leastsq(error,p0,args=(data_x,data_y))
        k,b = Para[0]
        return k,b
    
    def postpone_date(date,stock_trading_list):
        date_delta_list = [(i-date).days for i in stock_trading_list]
        delta_moreZero_list = [i for i in date_delta_list if i>=0]
        date_index = date_delta_list.index(sorted(delta_moreZero_list)[0])
        return stock_trading_list[date_index]
    
    if len(estimated_period) > 2 or len(windows_period) != 2:
        print('窗口期或估计期格式不正确')
        return -1
    #newdf = df.copy(deep = True) 
    if index_data_path[-5:] == '.xlsx':
        index_data = local_read_excel(index_data_path, code_col = '指数代码', collen_fill = index_collen_fill,time_col = [index_col[0]])
    elif type(index_data_path) == pd.core.frame.DataFrame:
        index_data = index_data_path.copy(deep=True)
    else:
        index_data = local_read_excel(''.join((index_data_path,index_code,'.xlsx')), collen_fill = index_collen_fill,code_col = '指数代码',time_col = [index_col[0]])
    tradingday_list = sorted([parse(i) for i in pd.read_excel(tradingday_data_path)[tradingday_col[0]].tolist()]) #所有的交易日数据
    code_list = list(set(df['股票代码'].tolist()))  #df公告数据涉及到的所有企业的股票代码
    newdf = pd.DataFrame(columns = df.columns.tolist()+[date_postpone_title]*sum([date_postpone])+['未计算原因','斜率','截距','R2','AdjR2']+[str(i) for i in range(windows_period[0],windows_period[1]+1)]+CAR_interval)         

    #新建一个df用于保存计算结果的数据,列是df的列加上拟合的斜率截距两项,再加上窗口期的每一天,再加上计算异常收益率的区间
    for code in code_list:
        #先读取该股票的个股回报率数据
        if stock_data_path[-5:] == '.xlsx':
            AllStockData = local_read_excel(stock_data_path, code_col = '股票代码',collen_fill = stock_collen_fill,time_col = [stock_col[0]])
            stock_data = AllStockData[AllStockData['股票代码']==code].copy().dropna(axis=0,subset=[stock_col[1]]).reset_index(drop=True)
        else:
            stock_data = local_read_excel(''.join((stock_data_path,code,'.xlsx')), code_col = '股票代码',collen_fill = stock_collen_fill,time_col = [stock_col[0]]).dropna(axis=0,subset=[stock_col[1]]).reset_index(drop=True)#从数据库中读取相应的数据文件
        stock_trading_list = sorted([parse(i) for i in stock_data[stock_col[0]].tolist()])#该企业的上市交易日期列表,注意到个股收益率数据是从时间最近到时间最远的,所以需要排序,改成从最早到最晚
        
        notice_dataset = df[df['股票代码']==code].copy(deep = True).reset_index(drop = True) #将当下股票代码的企业发布的公告全部复制然后赋给notice_dataset新数据集
        notice_dataset[date_title] = notice_dataset[date_title].apply(parse)
        notice_dataset = notice_dataset[notice_dataset[date_title]!=-1]
        if date_postpone:
            notice_dataset[date_postpone_title] = notice_dataset[date_title].apply(lambda x:postpone_date(x,stock_trading_list))
            new_date_title =  date_postpone_title
        else:
            new_date_title = date_title
        new_notice_dataset = pd.DataFrame(index = range(len(notice_dataset)),columns = newdf.columns.tolist()) #新建一个df用于保存计算结果的数据
        #new_notice_dataset行数和noticedataset相同,列是notice_dataset加上拟合的斜率截距两项,再加上窗口期的每一天,再加上计算异常收益率的区间
        for index in range(len(notice_dataset)):
            date = parse(notice_dataset.loc[index, new_date_title])
            date = datetime.datetime(date.year, date.month, date.day, 0, 0, 0) #因为指数\个股\交易日数据里面的日期均是按零时算的
            '''检验是否存在停牌情况'''
            if date in stock_trading_list and date in tradingday_list:
                if DateCheck(date, stock_trading_list, tradingday_list, estimated_period, windows_period, suspension_limit) == True: #停牌检查无误后开始进行线性拟合
                    reason = '已计算'
                    '''最小二乘法拟合得到市场模型中个股收益率和指数收益率的一次函数关系'''
                    #date_len = len(stock_data.loc[0,'交易日期']) #转换为str形式比较时间
                    relevant_stock_trading_date = [parse(i) for i in slice_list(date, stock_trading_list, estimated_period, interval_element = 'tuple')] #估计期,将所有元素都变成str方便后续定位
                    relevant_market_trading_date = [parse(i) for i in slice_list(date, tradingday_list, estimated_period, interval_element = 'tuple')]
                    estimated_date = [i for i in relevant_stock_trading_date if i in relevant_market_trading_date]
                    #estimated_date = [str(i)[:date_len] for i in slice_list(date, stock_trading_list, estimated_period, interval_element = 'tuple')] #估计期,将所有元素都变成str方便后续定位
                    data_y = np.array([stock_data[stock_data[stock_col[0]]==i][stock_col[1]].iloc[0] for i in estimated_date])
                    data_x = np.array([index_data[index_data[index_col[0]]==i][index_col[1]].iloc[0] for i in estimated_date])
                    
                    fit_result = sm.OLS(data_y, sm.add_constant(data_x)).fit()
                    b,k = fit_result.params#括号内因变量在前，自变量在后，结果截距在前，斜率在后
                    R2, AdjR2 = fit_result.rsquared, fit_result.rsquared_adj
                    '''根据计算出的k,b再计算窗口期内拟合收益率,进而得到异常收益率'''
                    windows_date = [parse(i) for i in slice_list(date, stock_trading_list, windows_period, interval_element = 'int')]
                    stock_return = [stock_data[stock_data[stock_col[0]]==i][stock_col[1]].iloc[0] for i in windows_date]
                    index_return = [index_data[index_data[index_col[0]]==i][index_col[1]].iloc[0] for i in windows_date]
                    #print(k,b)
                    AR_result = [] #用于保存窗口期内每一天的异常收益率
                    for i in range(len(windows_date)):
                        AR_result.append(stock_return[i]-(k*index_return[i]+b))
                    AR_result.extend(['']*(windows_period[1]-windows_period[0]+1-len(windows_date)))
                    '''根据异常收益率的计算结果计算,在CAR_interval中的CAR区间内的异常收益率'''
                    CAR_result = []
                    Day_list = list(range(windows_period[0],windows_period[1]+1))
                    for interval in CAR_interval:
                        left_margin = interval[0]
                        right_margin = interval[1] 
                        left_margin_index = Day_list.index(left_margin)
                        right_margin_index = Day_list.index(right_margin)
                        CAR_result.append(sum(AR_result[left_margin_index:right_margin_index+1])) #右边界+1是因为slice是左闭右开的，sum直接求和然后添入CAR_result
                else:
                    reason = DateCheck(date, stock_trading_list, tradingday_list, estimated_period, windows_period, suspension_limit)
            else:
                reason = '该日期企业未进行股票交易'
            if reason != '已计算':
                k,b = '',''
                R2, AdjR2 = '',''
                AR_result = ['']*(windows_period[1]-windows_period[0]+1)
                CAR_result = ['']*len(CAR_interval)
            new_notice_dataset.loc[index,:] = notice_dataset.loc[index,:].tolist() + [reason,k,b,R2,AdjR2] + AR_result + CAR_result
            print(code, date, reason)           
        new_notice_dataset = new_notice_dataset.dropna(how ='all')  
        newdf = pd.concat([newdf,new_notice_dataset]).reset_index(drop=True)
    return newdf 
    
index_dict = {'SH': '000913',
              'SZ': '000913',
              'HK': 'HSI',
              'NYA': 'NYA',
              'IXIC': 'IXIC'}
#def CAR_DifferentMarkets(df, market_col, index_dict, CAR_dict=CAR_dict, output ='divided', estimated_period = [(-128,-8)], windows_period = (-5,5), CAR_interval = [(-5,5),(-4,4),(-3,3),(-2,2),(-1,1),(-1,0),(0,1)], date_title = '公告发布日期', index_col = ['交易日期','指数回报率'], stock_col = ['交易日期','日个股回报率'], tradingday_col = ['交易日期'])：
def CAR_DifferentMarkets(df, market_col, index_dict, CAR_dict = CAR_dict, output ='divided', 
                         estimated_period = [(-128,-8)], windows_period = (-5,5), CAR_interval = [(-5,5),(-4,4),(-3,3),(-2,2),(-1,1),(-1,0),(0,1)],
                         date_title = '公告发布日期', index_col = ['交易日期','指数回报率'], stock_col = ['交易日期','日个股回报率'], tradingday_col = ['交易日期']):     
    newdf = df.copy()
    Markets = set(newdf[market_col]).intersection(set(list(index_dict)))
    resultdf = pd.DataFrame()
    residue = pd.DataFrame()
    for market in list(Markets):
        newdf_eachMarket = newdf[newdf[market_col] == market].reset_index(drop = True)
        if output == 'divided':
            CAR_eachMarket, Residue_eachMarket = CAR(newdf_eachMarket, index_code = index_dict[market], output = output, estimated_period = estimated_period , windows_period = windows_period, CAR_interval = CAR_interval, date_title = date_title, 
                                                     index_data_path = CAR_dict[market+'_index'], stock_data_path = CAR_dict[market+'_stock'], tradingday_data_path = CAR_dict[market+'_trading'], suspension_limit = 0,
                                                     index_col = index_col, stock_col = stock_col, tradingday_col = tradingday_col, market_col = market_col)
            resultdf = pd.concat([resultdf, CAR_eachMarket], ignore_index=True)
            residue = pd.concat([residue, Residue_eachMarket], ignore_index=True)
        if output == 'all':
            CAR_eachMarket = CAR(newdf_eachMarket, index_code = index_dict[market], output = output, estimated_period = estimated_period , windows_period = windows_period, CAR_interval = CAR_interval, date_title = date_title, 
                                 index_data_path = CAR_dict[market+'_index'], stock_data_path = CAR_dict[market+'_stock'], tradingday_data_path = CAR_dict[market+'_trading'], suspension_limit = 0,
                                 index_col = index_col, stock_col = stock_col, tradingday_col = tradingday_col, market_col = market_col)
            resultdf = pd.concat([resultdf, CAR_eachMarket], ignore_index=True)
    return resultdf, residue


