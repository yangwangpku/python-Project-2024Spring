import json
from pyecharts.charts import WordCloud
from pyecharts import options as opts

# Load the data from the JSON file
with open('maintainers_cooperation.json', 'r') as json_file:
    data = json.load(json_file)

# Extract project counts data
project_count_data = data["project_counts"]

# Prepare the data for the word cloud
wordcloud_data = [(item['maintainer'], item['project_count']) for item in project_count_data]

# Create the word cloud
wordcloud = (
    WordCloud()
    .add("", wordcloud_data, word_size_range=[20, 100])
    .set_global_opts(
        title_opts=opts.TitleOpts(title="Top Maintainers by Project Contributions"),
        tooltip_opts=opts.TooltipOpts(is_show=True),
    )
)

# Render the word cloud to an HTML file
wordcloud.render("maintainers_wordcloud.html")
