from pyecharts import Pie, Page, Style,Bar,Graph
import pandas as pd
import os,re,xlrd
import json
from pandas.io.json import json_normalize
from django.shortcuts import render,render_to_response
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import HttpResponse  # 导入HttpResponse模块

def countit(dd):
    res={}
    for d in dd:
        try:
            res[d]=res[d]+1
        except:
            res[d]=1
    try:
        res['其他']+=res.pop('无')
    except:
        res['其他']=res.pop('无')
    return res

def create_charts_pie():
    #pie
    page = Page()

    style = Style(
        width=1100, height=900
    )
    data=pd.read_csv('/Users/fxm/PycharmProjects/fo/data/结果/名+标点_class_1213.csv')
    ks1,vs1=[],[]
    for k,v in countit(data['d'].values).items():
        ks1.append(k)
        vs1.append(v)
    ks2,vs2=[],[]
    for k,v in countit(data['e'].values).items():
        ks2.append(k)
        vs2.append(v)
    chart = Pie("类别分布", title_pos='center', **style.init_style)
    chart.add("", ks2, vs2,
              radius=[60, 80], is_label_show=True,is_legend_show=False)
    chart.add("", ks1,vs1, radius=[0, 50], is_label_show=True,is_legend_show=False,label_pos='inside')
    page.add(chart)

    return page

def create_charts():
    page = Page()

    style = Style(
        width=900, height=600,title_pos='center'
    )
    w='雷音'
    res={}

    for rt, ds, ffs in os.walk('/Users/fxm/经语料/T_out/'):
        for d in ds:
            if int(d.replace('T',''))<18:
                for rr,dd,ff in os.walk(rt+d):
                    for f in ff:
                        with open(rr+'/'+f,encoding='utf8') as file:
                            ss=file.read()
                            jm = re.search('title:(.*)\s', ss).group(1)
                            try:
                                res[jm]+=ss.count(w)
                            except:
                                res[jm]=ss.count(w)
    res=sorted(res.items(),key=lambda x:x[1],reverse=True)[:50]
    attr = [x[0] for x in res]
    v1 = [x[1] for x in res]
    chart = Bar("雷音-經目出現頻次圖", **style.init_style)
    # chart.add("", attr, v1, xaxis_interval=0, xaxis_rotate=30,yaxis_rotate=30)
    chart.add("", attr, v1, is_label_show=True, is_datazoom_show=True, xaxis_rotate=30,xaxis_interval=0)
    page.add(chart)
    return page

def duidie():
    page = Page()
    style = Style(
        width=800, height=600, title_pos='left'
    )

    # data=pd.read_csv('/Users/fxm/PycharmProjects/fo/data/结果/名+标点_class_1213.csv')
    # res={}
    # for rt, ds, ffs in os.walk('/Users/fxm/经语料/T_out/'):
    #     for d in ds:
    #         if int(d.replace('T',''))<18:
    #             for rr,dd,ff in os.walk(rt+d):
    #                 for f in ff:
    #                     with open(rr+'/'+f,encoding='utf8') as file:
    #                         ss=file.read()
    #                         jm = re.search('title:(.*)\s', ss).group(1)
    #                     for rm in data[data['d']=='人物']['a'].values:
    #                         if not str(rm).isdigit():
    #                             try:
    #                                 res[jm][0]+=ss.count(rm)
    #                             except:
    #                                 res[jm]=[ss.count(rm),0,0]
    #                     for rm in data[data['d']=='地名']['a'].values:
    #                         if not str(rm).isdigit():
    #                             try:
    #                                 res[jm][1]+=ss.count(rm)
    #                             except:
    #                                 res[jm]=[0,ss.count(rm),0]
    #                     for rm in data[data['d']=='其他']['a'].values:
    #                         if str(rm)!='nan':
    #                             try:
    #                                 res[jm][2]+=ss.count(rm)
    #                             except:
    #                                 print(rm)
    #                                 res[jm]=[0,0,ss.count(rm)]
    f = open('temp.txt', 'r')
    a = f.read()
    res = eval(a)
    f.close()
    print('_____')
    res=sorted(res.items(),key=lambda x:sum(x[1]),reverse=True)[:30]
    attr,v1,v2,v3=[],[],[],[]
    for k,v in res:
        attr.append(k)
        v1.append(v[0])
        v2.append(v[1])
        v3.append(v[2])

    chart = Bar("经目-词频堆叠", **style.init_style)
    chart.add("人名", attr, v1, is_stack=True,xaxis_interval=0,xaxis_rotate=30,yaxis_max=450000)
    chart.add("地名", attr, v2, is_stack=True,is_more_utils=True,xaxis_interval=0,xaxis_rotate=30,yaxis_max=450000)
    chart.add("其他", attr, v3, is_stack=True,is_more_utils=True,xaxis_interval=0,xaxis_rotate=30,yaxis_max=450000)
    page.add(chart)
    return page
def count_per(w):
    page = Page()
    style = Style(
        width=900, height=600, title_pos='center'
    )
    res = {}
    for rt, ds, ffs in os.walk('/Users/fxm/经语料/T_out/'):
        for d in ds:
            if int(d.replace('T', '')) < 18:
                for rr, dd, ff in os.walk(rt + d):
                    for f in ff:
                        with open(rr + '/' + f, encoding='utf8') as file:
                            ss = file.read()
                            jm = re.search('title:(.*)\s', ss).group(1)
                            try:
                                res[jm] += ss.count(w)
                            except:
                                res[jm] = ss.count(w)
    res = sorted(res.items(), key=lambda x: x[1], reverse=True)[:50]
    attr = [x[0] for x in res]
    v1 = [x[1] for x in res]
    chart = Bar(w+"-經目出現頻次圖", **style.init_style)
    # chart.add("", attr, v1, xaxis_interval=0, xaxis_rotate=30,yaxis_rotate=30)
    chart.add("", attr, v1, is_label_show=True, is_datazoom_show=True, xaxis_rotate=30, xaxis_interval=0)
    page.add(chart)
    return page


def relation(node=None):
    # data=pd.read_csv('/Users/fxm/经语料/经语料/成果/图/词典-繁体.csv',encoding='utf8')
    # cds= pd.read_csv('/Users/fxm/经语料/经语料/成果/人名朝代表格.csv',encoding='utf8')
    # cds.columns=['A','B','C','D']
    # data.columns=['A','B','C']
    # nodes,links = [],[]
    # for l in data[data['B']!='地名'].values:
    #     if str(l[2])!='nan':
    #         x=re.search('[^\u4e00-\u9fa5]([\u4e00-\u9fa5]*)(之女|之二子|之子|最後之一子|弟名|之太子|之夫人|妻之名|女之名|子之名|之長者子|二子之一)[^\u4e00-\u9fa5]','。'+l[2])
    #         if x:
    #             nodes.append({"name": str(l[0]), "symbolSize": 10, "category": 1,'value':'人物'})
    #             nodes.append({"name":x.groups()[0], "symbolSize": 10, "category": 1,'value':'人物'})
    #             links.append({"source":l[0],"target":x.groups()[0],"value":x.groups()[1]})
    #             print(x.groups()[1])
    #         x = re.search('[^\u4e00-\u9fa5]([\u4e00-\u9fa5]{2,8})人[^\u4e00-\u9fa5]', '。' + l[2])
    #         if x:
    #             nodes.append({"name": str(l[0]), "symbolSize": 10, "category": 1,'value':'人物'})
    #             if x.groups()[0].find('之夫人')==-1:
    #                 nodes.append({"name": x.groups()[0], "symbolSize": 10, "category": 2})
    #                 links.append({"source":l[0],"target":x.groups()[0],"value":'故乡'})
    #         x = re.search('[^\u4e00-\u9fa5]初住([\u4e00-\u9fa5]{2,8})[^\u4e00-\u9fa5]', '。' + l[2])
    #         if x:
    #             nodes.append({"name": str(l[0]), "symbolSize": 10, "category": 1,'value':'人物'})
    #             nodes.append({"name": x.groups()[0], "symbolSize": 10, "category": 2})
    #             links.append({"source": l[0], "target": x.groups()[0], "value": '住所'})
    #         x = re.search('[^\u4e00-\u9fa5]後住([\u4e00-\u9fa5]{2,8})[^\u4e00-\u9fa5]', '。' + l[2])
    #         if x:
    #             nodes.append({"name": str(l[0]), "symbolSize": 10, "category": 1,'value':'人物'})
    #             nodes.append({"name": x.groups()[0], "symbolSize": 10, "category": 2})
    #             links.append({"source": l[0], "target": x.groups()[0], "value": '住所'})
    #         else:
    #             x = re.search('[^\u4e00-\u9fa5][住居]([\u4e00-\u9fa5]{2,8})[^\u4e00-\u9fa5]', '。' + l[2])
    #             if x:
    #                 nodes.append({"name": str(l[0]), "symbolSize": 10, "category": 1,'value':'人物'})
    #                 nodes.append({"name": x.groups()[0], "symbolSize": 10, "category": 2})
    #                 links.append({"source": l[0], "target": x.groups()[0], "value": '住所'})
    #         x = re.search('[^\u4e00-\u9fa5]([\u4e00-\u9fa5]{2,8})之一[^\u4e00-\u9fa5]', '。' + l[2])
    #         if x:
    #             nodes.append({"name": str(l[0]), "symbolSize": 10, "category": 1,'value':'人物'})
    #             nodes.append({"name": x.groups()[0], "symbolSize": 10, "category": 0})
    #             links.append({"source": l[0], "target": x.groups()[0], "value": '属于'})
    #
    # nodes1,links1=[],[]
    # names1,nodes2=[],[]
    # for d in nodes:
    #     if d["name"] not in names1:
    #         names1.append(d["name"])
    #         nodes1.append(d)
    # for d in nodes1:
    #     resss=cds[cds['C']==d['name']]
    #     if not resss.empty:
    #         if {"name": str(resss.values[0][0]), "symbolSize": 10, "category": 3,'value':'朝代'} not in nodes2:
    #             nodes2.append({"name": str(resss.values[0][0]), "symbolSize": 10, "category": 3,'value':'朝代'})
    #         links.append({"source": d["name"], "target": resss.values[0][0], "value": '朝代地区'})
    # nodes1+=nodes2
    # names1,nodes3=[],[]
    # for d in nodes1:
    #     if d["name"] not in names1:
    #         names1.append(d["name"])
    #         nodes3.append(d)
    # for d in links:
    #     if d not in links1:
    #         links1.append(d)
    # with open('../data/relation.josn','w',encoding='utf8') as f:
    #     json.dump((nodes3, links1),f)
    with open('/Users/fxm/PycharmProjects/gra_fo/data/relation.json','r',encoding='utf8') as f:
        nodes3, links1=json.load(f)
    if node and node!='':
        df_nodes=json_normalize(nodes3)
        df_links=json_normalize(links1)
        nodes3,links1=[],[]
        bur=[node]
        burall=bur.copy()
        nn = bur.pop(0)
        if df_nodes[df_nodes['name'] == nn].empty:
            page = Page()
            return page
        if str(nn) != 'nan':
            # print(nn)
            l = df_nodes[df_nodes['name'] == nn][['category', 'value']].values
            nodes3.append({"name": nn, "symbolSize": 20, "category": int(l[0][0]), 'value': str(l[0][1])})
            for x in df_links[df_links['source'] == nn][['source', 'target', 'value']].values:
                if x[1] not in burall:
                    bur.append(x[1])
                    burall.append(x[1])
                if {"source": x[0], "target": x[1], "value": x[2]} not in links1:
                    links1.append({"source": nn, "target": x[1], "value": x[2]})
            for x in df_links[df_links['target'] == nn][['source', 'target', 'value']].values:
                if x[0] not in burall:
                    bur.append(x[0])
                    burall.append(x[0])
                if {"source": x[0], "target": x[1], "value": x[2]} not in links1:
                    links1.append({"source": x[0], "target": x[1], "value": x[2]})
        while bur:
            nn=bur.pop(0)
            if str(nn)!='nan':
                # print(nn)
                l=df_nodes[df_nodes['name']==nn][['category','value']].values
                nodes3.append({"name":nn, "symbolSize": 10, "category": int(l[0][0]),'value':str(l[0][1])})
                for x in df_links[df_links['source']==nn][['source','target','value']].values:
                    if x[1] not in burall:
                        bur.append(x[1])
                        burall.append(x[1])
                    if {"source":x[0], "target": x[1], "value": x[2]} not in links1:
                        links1.append({"source":nn, "target": x[1], "value": x[2]})
                for x in df_links[df_links['target']==nn][['source','target','value']].values:
                    if x[0] not in burall:
                        bur.append(x[0])
                        burall.append(x[0])
                    if {"source":x[0], "target": x[1], "value": x[2]} not in links1:
                        links1.append({"source":x[0], "target": x[1], "value": x[2]})

    # print(nodes1)
    # nodes2=[{'name': '1', 'symbolSize': 100, 'category': 1},{'name': '2', 'symbolSize': 100, 'category': 0}]
    # links1=[{"source":'1', "target": '2', "value": 1}]
    page = Page()
    categories = [0,1,2,3]
    graph = Graph("",width=1200, height=600)
    # graph.use_theme('chalk')
    graph.add("", nodes3, links1, categories,
              is_focusnode=True,
              is_roam=True,
              is_rotatelabel=False,
              label_pos="right",
              repulsion=100,
              line_curve=0,
              legend_text_size=10,
              )
    page.add(graph)
    return page

def class_re(request):
    name=request.session.get('nn')
    with open("/Users/fxm/PycharmProjects/gra_fo/data/人物共现.json", "r", encoding='utf-8') as f1:
        Data = json.load(f1)
    jing=''
    juan=''
    for i in Data:
        if i["name"] == name:
            jing = i["经号"]
            juan = i["卷号"]
            lei = i["类别"]
            Data.remove(i)

    nodes, links = [{"name": name, "symbolSize": 10, "category": 0}], []
    nodes1, links1 = [{"name": name, "symbolSize": 10, "category": 0}], []
    nodes2, links2 = [{"name": name, "symbolSize": 10, "category": 0}], []
    nodes3, links3 = [{"name": name, "symbolSize": 10, "category": 0}], []
    categories = [0, 1, 2]

    for i in Data:
        if i["经号"] == jing:
            node = {}
            link = {}
            node["name"] = i["name"]
            node["symbolSize"] = 5
            node["category"] = 1
            link["source"] = name
            link["target"] = i["name"]
            link["value"] = i["经号"]
            if i["卷号"] == juan:
                node["symbolSize"] = 10
                node["category"] = 0
                link["value"] = i["卷号"]
            nodes.append(node)
            links.append(link)
            if i["类别"] == "王":
                # or"龍王"or"王子"
                nodes1.append(node)
                links1.append(link)
            elif i["类别"] == "佛" or i["类别"] == "如來":
                # "佛"or
                nodes2.append(node)
                links2.append(link)
            else:
                nodes3.append(node)
                links3.append(link)

    a = len(nodes) - 1
    b = len(nodes1) - 1
    c = len(nodes2) - 1
    d = len(nodes3) - 1
    print("共发现与%s同经或同卷共现人物%s个，其中王类%s个，佛类%s个，其他类%s个" % (name, a, b, c, d))
    # 生成图谱，同卷共现的颜色相同
    page = Page()
    graph = Graph("经卷共现图谱", width=1200, height=600, )
    # graph.use_theme('chalk')
    graph.add("", nodes, links, categories,
              is_focusnode=True,
              is_roam=True,
              is_rotatelabel=False,
              label_pos="right",
              repulsion=100,
              line_curve=0,
              legend_text_size=10,
              )
    page.add(graph)
    graph1 = Graph("王类", width=1200, height=600, )
    # graph1.use_theme('chalk')
    graph1.add("", nodes1, links1, categories,
               is_focusnode=True,
               is_roam=True,
               is_rotatelabel=False,
               label_pos="right",
               repulsion=100,
               line_curve=0,
               legend_text_size=10,
               )
    page.add(graph1)
    graph2 = Graph("佛类", width=1200, height=600, )
    # graph2.use_theme('chalk')
    graph2.add("", nodes2, links2, categories,
               is_focusnode=True,
               is_roam=True,
               is_rotatelabel=False,
               label_pos="right",
               repulsion=100,
               line_curve=0,
               legend_text_size=10,
               )
    page.add(graph2)
    graph3 = Graph("其他", width=1200, height=600, )
    # graph3.use_theme('chalk')
    graph3.add("", nodes3, links3, categories,
               is_focusnode=True,
               is_roam=True,
               is_rotatelabel=False,
               label_pos="right",
               repulsion=100,
               line_curve=0,
               legend_text_size=10,
               )
    page.add(graph3)
    x_axis = ["王类", "佛类", "其他"]
    y_axis = [a, b, c]
    bar = Bar("分类柱状图", width=1200, height=600)
    # bar.use_theme('chalk')
    bar.add("", x_axis, y_axis)
    page.add(bar)
    page.render(path="/Users/fxm/PycharmProjects/gra_fo/templates/class_re.html")
    return render(request,"index.html",{'inner':'class_re'})

def gongxian(request):
    # 将excel转为列表形式 [{"name":name,"jingmu":[xx经，xx经,]}, , ,]
    name=request.session.get('nn')
    data = xlrd.open_workbook("/Users/fxm/PycharmProjects/gra_fo/data/短篇分词回收人名与经目.xlsx")
    table = data.sheets()[0]
    nrows = table.nrows
    list = []
    for i in range(1, nrows):
        newdata = {}
        content = table.row_values(i)
        newdata["name"] = content[0]
        newdata["经目"] = []
        for j in range(2, 40):
            if content[j] is "":
                break
            newdata["经目"].append(content[j])
        list.append(newdata)

    list1 = []  # 存放一级相关节点
    list2 = []  # 存放二级相关节点

#构造节点及连线
    nodes = [{"name": name, "symbolSize": 15, "category": 0}]
    links = []
    categories = [0, 1, 2]
    # 取与输入人物同经共现的一级人物节点
    for i in list:
        if i["name"] == name:
            list.remove(i)
            for j in list:
                for x in i["经目"]:
                    for y in j["经目"]:
                        if x == y and j not in list1:
                            node = {}
                            node["name"] = j["name"]
                            node["symbolSize"] = 10
                            node["category"] = 1
                            nodes.append(node)
                            link = {}
                            link["source"] = i["name"]
                            link["target"] = j["name"]
                            link["value"] = x
                            links.append(link)
                            list.remove(j)
                            list1.append(j)

    # 对一级共现人物节点取同经共现人物
    for i in list1:
        for j in list:
            for x in i["经目"]:
                for y in j["经目"]:
                    if x == y and {"name": j["name"], "symbolSize": 5, "category": 2} not in nodes:
                        node = {}
                        node["name"] = j["name"]
                        node["symbolSize"] = 5
                        node["category"] = 2
                        nodes.append(node)
                        link = {}
                        link["source"] = i["name"]
                        link["target"] = j["name"]
                        link["value"] = x
                        links.append(link)
                        list.remove(j)
                        list2.append(j)
    a = len(list1)
    b = len(list2)
    # 生成关系图
    page = Page()
    graph = Graph("二级共现人物", width=1200, height=600)
    # graph.use_theme('chalk')
    graph.add("", nodes, links, categories,
              is_focusnode=True,
              is_roam=True,
              is_rotatelabel=False,
              label_pos="right",
              repulsion=100,
              line_curve=0,
              legend_text_size=10,
              )
    page.add(graph)
    # bar图
    x_axis = ["一级共现", "二级共现"]
    y_axis = [a, b]
    bar = Bar("同经共现", width=1200, height=600)
    # bar.use_theme('chalk')
    bar.add("", x_axis, y_axis, bar_category_gap='50%', )
    page.add(bar)
    page.render(path="/Users/fxm/PycharmProjects/gra_fo/templates/render_all.html")
    return render(request,"index.html",{'inner':'gongxian'})

def html_class(class_re):
    return render_to_response("class_re.html")
def test(requst):
    return render_to_response("index.html")

def html_count(requst):
    return render_to_response("render_count.html")
def html_gongxian(requst):
    return render_to_response("render_all.html")
def html_relation(requst):
    return render_to_response("render_relation.html")

@csrf_exempt
def index(request):
    x=request.POST.get("qq",None)
    request.session['nn'] =x
    count_per(x).render('/Users/fxm/PycharmProjects/gra_fo/templates/render_count.html')
    return render(request,"index.html",{'inner':'count'})

@csrf_exempt
def relation_s(request):
    # x=request.POST.get("qq",None)
    x=request.session.get('nn')
    relation(x).render('/Users/fxm/PycharmProjects/gra_fo/templates/render_relation.html')
    return render(request,"index.html",{'inner':'relation'})

# create_charts_pie().render('../data/render_leibie.html')
