# 清洗标题内容 如抖音包含标签的删除标签， 若删完标签后标题为空，则不要对应视频
class Cleaner_Title:
    douyin_tags = [
        '#股票', '#股市投资', '#财经', '#金融', '#基金', '#干货', '#财经知识', '#金融',
        '#财经', '#理财', '#股民','#投资', '#干货分享', '#财经知识', '#创作灵感', '#换手率',
        '#股票', '#主力', '#金融', '#量化', '#量化交易', '#股市', '#上证指数','#投资理财',
        '#芬钛计划', '#知识点总结', '@DOU+小助手', '#期货', '#韭菜', '#中银绒业', '#A股', '#收盘',
        '#油价', '#一分钟读懂财经', '#配资', '#超短线', '#情绪接力', '#我要上头条', '#商业思维', '#股民',
        '#短线',
    ]
    @classmethod
    def clean_douyin(cls, title):
        '''
        清洗抖音的标题
        包含标签的删除标签， 若删完标签后标题为空，则不要对应视频
        '''
        for tag in cls.douyin_tags:
            if(tag in title):
                title = title.replace(tag, '')
            else:
                continue
        return title

    @classmethod
    def clean_douyin_method2(cls, title):
        if ('#' in title):
            title = title[:title.index('#')]
        return title
