import json
from pyecharts.charts import Bar, Tab
from pyecharts import options as opts

# Load the data from the JSON file
with open('language_counts_by_topic.json', 'r') as json_file:
    data = json.load(json_file)

# List of specified languages to maintain the order
languages_of_interest = ["C", "C++", "Cython", "JavaScript", "SQL", "Fortran", "Rust", "Unix Shell"]

# Initialize a Tab object
tab = Tab()

# Create a bar chart for each topic and add it to the tab
for topic, language_data in data.items():
    bar = (
        Bar()
        .add_xaxis(languages_of_interest)
        .add_yaxis(
            "Project Count", 
            [language_data.get(language, 0) for language in languages_of_interest],
            label_opts=opts.LabelOpts(position="top")
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title=f"Project Count by topic for {topic} (Excluding Python)"),
            xaxis_opts=opts.AxisOpts(name="Languages"),
            yaxis_opts=opts.AxisOpts(name="Project Count"),
            toolbox_opts=opts.ToolboxOpts(is_show=True),
            legend_opts=opts.LegendOpts(is_show=False),
            datazoom_opts=[
                opts.DataZoomOpts(type_="slider", is_show=True, xaxis_index=0, range_start=0, range_end=100),
                opts.DataZoomOpts(type_="inside", xaxis_index=0, range_start=0, range_end=100)
            ]
        )
    )
    tab.add(bar, topic)

# Render the chart to an HTML file
tab.render("languages_by_topic.html")
