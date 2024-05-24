import json
import math
from pyecharts.charts import Graph
from pyecharts import options as opts

# Load the data from the JSON file
with open('maintainers_cooperation.json', 'r') as json_file:
    data = json.load(json_file)

# Extract cooperation and project counts data
cooperation_data = data["cooperation"]
project_count_data = data["project_counts"]

# Create a set of maintainers who have cooperations
cooperating_maintainers = set()
for item in cooperation_data:
    cooperating_maintainers.add(item["maintainer1"])
    cooperating_maintainers.add(item["maintainer2"])

# Prepare nodes and links for the graph
nodes = []
links = []

# Create a dictionary to map maintainers to their project counts
project_counts = {item['maintainer']: item['project_count'] for item in project_count_data}

# Create nodes for maintainers who have cooperations
for maintainer, project_count in project_counts.items():
    if maintainer in cooperating_maintainers:
        nodes.append({
            "name": maintainer,
            "symbolSize": math.log10(project_count) * 15,  # Adjust the size based on project count
            "value": project_count
        })

# Create links for maintainers who have cooperations
for item in cooperation_data:
    if item["maintainer1"] in cooperating_maintainers and item["maintainer2"] in cooperating_maintainers:
        links.append({
            "source": item["maintainer1"],
            "target": item["maintainer2"],
            "value": item["project_count"],
            "lineStyle": {"width": math.log10(item["project_count"]+1)},  # Adjust the width based on cooperation count
            "distance": math.log10(item["project_count"] + 1) * 10
        })

# Create the graph
graph = (
    Graph(init_opts=opts.InitOpts(width="1000px", height="600px"))
    .add(
        "",  # Series name
        nodes,
        links,
        repulsion=4000,  # Adjust repulsion to space out nodes
        edge_length=[10, 50],  # Edge length adjustment
        layout="force",  # Use force-directed layout
        gravity=2,
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="Cooperation Between Top 50 Maintainers"),
        tooltip_opts=opts.TooltipOpts(trigger="item", formatter="{b}: {c}")
    )
)

# Render the graph to an HTML file
graph.render("maintainers_cooperation_graph.html")
