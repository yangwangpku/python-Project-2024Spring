"""
Date: 2021.3.22
Author: Justin

要点说明：
Map 地图
在世界地图上填充区域色块

参考pyecharts 官方文档
"""

from pyecharts.faker import Faker
from pyecharts import options as opts
from pyecharts.charts import Map
import json

# load data from population_world.json
data = json.load(open('./data/population_world.json', 'r', encoding='utf-8'))
map_data = list(data.items()) 

c = (
    Map()
    .add("2023年世界各国家人口",
         data_pair=map_data,
         maptype="world",
         is_map_symbol_show=False, # 不描点    
         tooltip_opts=opts.TooltipOpts(formatter="{b}: {c}"),  # 设置 tooltip 格式，{b} 表示城市名称，{c} 表示数值         
    )
    .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    .set_global_opts(
        title_opts=opts.TitleOpts(title="2023年世界各国家人口"),
        visualmap_opts=opts.VisualMapOpts(max_=200000000),
    )
)

c.render('./homework1/population_world_map.html')