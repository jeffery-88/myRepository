from pyecharts.charts import Geo
from pyecharts import options
from pyecharts.globals import GeoType

import pandas as pd
import requests
import csv
import json
from urllib.request import urlopen

import geopandas
import os

import geopandas as gpd
import matplotlib.pyplot as plt


AK = "wLOHeWMwAw1LLBY3dG3LBRrerwan0Dd3"

def get_jason_api():
    req = urlopen('https://geo.datav.aliyun.com/areas_v3/bound/310000_full.json')
    res = req.read().decode()
    temp = json.loads(res)
    # 保存上海.json
    with open("./上海.json", 'w', encoding='utf-8') as json_file:
        json.dump(temp, json_file, ensure_ascii=False)

def saveShapefile(file_name,output_shapefile_name):
    try:
        data = geopandas.read_file(file_name)
        localPath = str(output_shapefile_name)
        data.to_file(localPath, driver='ESRI Shapefile', encoding='gbk')
        print("转化成功,文件存放位置："+localPath)
    except:
        print("转化失败")

def generate_map(position):
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    # 输入图名
    Map_name = '上海'
    regions = gpd.GeoDataFrame.from_file('./上海/上海.shp', encoding='gbk')
    regions['coords'] = regions['geometry'].apply(lambda x: x.representative_point().coords[0])
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_aspect('equal')
    regions.plot(ax=ax, column='name', legend=False,
                 cmap='Pastel1_r',
                 edgecolor='k')
    # # 地图标注
    # for n, i in enumerate(regions['coords']):
    #     plt.text(i[0]-0.15, i[1], regions['name'][n], fontsize=8, horizontalalignment="left")  # 标注位置X，Y，标注内容
    # 地图点标注
    plt.plot(ax=ax, marker='o', color='red', markersize=50)
    # 地区名标注
    ax.text(position[0], position[1], "高宝路229弄", fontsize=11, horizontalalignment="left")

    ax.set_title('Python-{}地图'.format(Map_name), fontsize=18, fontweight='bold')
    plt.grid(True, alpha=0.5)  # 显示网格，透明度为50%
    # ax.set_axis_off()
    plt.show()


def get_position(name, AK):
    url = f'http://api.map.baidu.com/geocoding/v3/?address={name}&output=json&ak={AK}'
    res = requests.get(url)
    val = res.json()
    retval = {'地址':name,
              '经度':val['result']['location']['lng'],
              '纬度':val['result']['location']['lat'],
              '地区标签':val['result']['level'],
              '是否精确招到':val['result']['precise']}
    longitude = retval['经度']
    latitude = retval['纬度']
    return(longitude, latitude)


def locate_on_map(addr,longtitude,latitude):
    g = Geo().add_schema(maptype="上海")
    g.add_coordinate(addr, longtitude, latitude)
    data_pair = [(addr, 1)]
    g.add('', data_pair, type_=GeoType.EFFECT_SCATTER, symbol_size=20)
    g.set_series_opts(label_opts=options.LabelOpts(is_show=False))
    g.set_global_opts(title_opts=options.TitleOpts(title="地图标点测试"))

    g.render_notebook()
    print("process finished")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    addr = ['上海市浦东新区高宝路229弄', '上海市浦东新区金苏路200号', '上海市浦东新区新金桥路2222号']
    for i in addr:
        position = get_position(i, AK)
        print("current addr is " + str(i))
        print("longtitude is " + str(position[0]) + "latitude is " + str(position[1]) + '\n')
    print(position)
    print("############position")
    get_jason_api()
    saveShapefile('上海.json', '上海')
    generate_map(position)
    locate_on_map(addr[0], position[0], position[1])


