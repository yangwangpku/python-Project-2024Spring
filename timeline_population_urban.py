from pyecharts import options as opts
from pyecharts.charts import Bar, Page, Pie, Timeline
import json

file = json.load(open('./data/population_city.json', 'r', encoding='utf-8'))
cities = file["cities"]
data = file["data"]
tl = Timeline()

for i in range(2016, 2023):
    bar = (
        Bar()
        .add_xaxis(cities)
        .add_yaxis("人口", data[str(i)])
        .set_global_opts(
            title_opts=opts.TitleOpts("{}年各城市人口".format(i)),
            yaxis_opts=opts.AxisOpts(max_=15000)  # 设置纵坐标轴的最大值
        )
    )
    tl.add(bar, "{}年".format(i))

tl.render('./homework1/population_city.html')


    