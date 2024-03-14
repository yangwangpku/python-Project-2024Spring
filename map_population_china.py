"""
Date: 2021.3.22
Author: DEER

要点说明：
用map画出全国人口图
"""
from pyecharts.faker import Faker
from pyecharts import options as opts
from pyecharts.charts import Map
import json

# 2023年全国人口数据

# load data from population_china.json
data = json.load(open('./data/population_china.json', 'r', encoding='utf-8'))
map_data = list(data.items()) 

c = (
    Map()
    .add("2023年中国各省份人口（单位：万）", 
         data_pair=map_data, 
         maptype="china",
         is_map_symbol_show=False, # 不描点    
         tooltip_opts=opts.TooltipOpts(formatter="{b}: {c} 万"),  # 设置 tooltip 格式，{b} 表示城市名称，{c} 表示数值         
    )
    
    .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    .set_global_opts(
        title_opts=opts.TitleOpts(title="2023年中国各省份人口"),
        visualmap_opts=opts.VisualMapOpts(min_=0, max_=12000),
    )
)

c.render('./homework1/population_china_map.html')