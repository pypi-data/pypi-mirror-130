from basement__.IsCheck import IsCheck_uchar
'''
    清洁器 基类
    所有定制化清洁器都继承自该类
'''
class Base_Cleaner:
    cleanWordList = []     # 清洗词列表，存放准备清洗掉的字符/字符串

    irrelevantWordList = ['图']     # 杂七杂八的无规律可循不相关的文字 如： 图9-5
    cleanWordList_headnum = []  # 序号列表

    # 通用的待组合清洗字符字典列表，如数字、字母等
    universal_cleanWordDict = {
        'alphabeticList':[
            'A','B','C','D','E','F','G','H'
        ],
        'numList1':['一','二','三','四','五','六','七','八','九','十'],
        'numList2':['第一','第二','第三','第四','第五','第六','第七','第八','第九','第十'],
    }

    # 清洗掉空格和结尾的空格
    @staticmethod
    def delSpace(paragraph:str):
        return paragraph.replace("\r", "").replace("\n", "").replace("\t", "").replace("\xa0", "").replace("\u3000", "")

    # 删除开头的序号 如 1. 2. 1、 2、 1， 2，
    @staticmethod
    def delHeaderNum(paragraph:str, cleanWordList:list):
        '''
        清除段落头尾数字
        :param paragraph: 待清洗的字符串
        :param cleanWordList: 待清除的字符串
        :return: 清洗后的字符串
        '''
        for cleanword in cleanWordList:
            if (paragraph.startswith(cleanword)):
                paragraph = paragraph[len(cleanword):]
                break
        return paragraph

    # 删除股票名字和股票代码
    @staticmethod
    def delStocksNameAndCode(paragraph, stocksNameCodeList):
        '''
        （用于段落字符串清洗）清除字符串中的股票名/股票代码
        :param paragraph:
        :param stocksNameCodeList:
        :return:
        '''
        for item in stocksNameCodeList:
            li = []
            li.append(item[0] + "（{}）".format(item[1]))
            li.append("（{}）".format(item[0]))
            li.append("（{}）".format(item[1]))
            li.append(item[0])
            li.append(item[1])
            for stock in li:
                paragraph = paragraph.replace(stock, "")  # 删除股票关键字（包括中文及代买关键字）
        return paragraph

    # 删除杂七杂八的无规律可循不相关的文字 如： 图9-5
    @staticmethod
    def delIrrelevantWord(paragraph, irrelevantWordList):
        # irrelevantWordList = ['图']
        for irrelevantWord in irrelevantWordList:
            paragraph = paragraph.replace(irrelevantWord, "")
        return paragraph

    @staticmethod
    def del_webTag(comment):
        '''
        (针对爬取的评论内容设计的方法) 清除评论内容中有标签内容的
        :param comment:
        :return:
        '''
        s = ''
        for m in comment.split('>'):
            s = s + m.split('<')[0]
        return s

    @staticmethod
    def del_repeatstr(s):
        """去除重复字符串中重复的(
            注意：该功能只针对中文内容和符号以及英文内容，对数字的重复不进行清洗
            )
        """
        cleaned_s = ''
        for i in range(len(s)):
            if (i < len(s) - 1):
                if(IsCheck_uchar.is_number(s[i])):
                    cleaned_s = cleaned_s + s[i]
                elif(s[i] != s[i + 1]):
                    cleaned_s = cleaned_s + s[i]
                else:
                    continue
            elif (i == len(s) - 1):
                cleaned_s = cleaned_s + s[i]
            else:
                break
        return cleaned_s

    def integratedOp(self, paragraph):
        '''
        集成操作方法 输出的结果为最终清洗完成的结果 又子类重写定制
        :param paragraph: 待清洗的字符串
        :return: paragraph: 经过一系列自定义清洗后的
        '''
        print('未设置集成方法')
        # # 清序号
        # temp = self.delHeaderNum(paragraph)
        # # 清空格
        # temp = self.delSpace(temp)
        # # 清序号
        # temp = self.delHeaderNum(temp)
        # # 清股票
        # # temp = self.delStocksNameAndCode(temp)
        # # 清不相关的文字
        # result = self.delIrrelevantWord(temp)
        # return result
        pass






