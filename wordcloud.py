import jieba
from pyecharts.charts import WordCloud
import jieba.posseg as pseg

# 读取文本文件
def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text

# 使用jieba进行分词并识别命名实体
def tokenize_and_recognize_entities(text):
    words_with_entities = []
    words = pseg.cut(text)
    for word, flag in words:
        # 只保留词性为nr（人名）、ns（地名）、nt（机构名）的词语
        if flag in ['nr', 'ns', 'nt']:
            words_with_entities.append(word)
    return words_with_entities

# 统计词频
def count_word_frequency(word_list, min_length=2):
    word_freq = {}
    for word in word_list:
        if len(word) < min_length:
            continue
        if word in word_freq:
            word_freq[word] += 1
        else:
            word_freq[word] = 1
    return word_freq

# 生成词云
def generate_word_cloud(word_freq, output_file):
    # transform word_freq to list of tuples
    word_freq = list(word_freq.items())

    # sort the list by word frequency
    word_freq.sort(key=lambda x: x[1], reverse=True)

    cloud = WordCloud()
    cloud.add('', word_freq[:50])
    cloud.render(output_file)

if __name__ == "__main__":
    file_path = 'data/西游记.txt'  # 替换为你的文件路径
    output_file = 'homework1/wordcloud.html'  # 生成的词云图文件路径
    text = read_text_file(file_path)
    words_with_entities = tokenize_and_recognize_entities(text)
    word_freq = count_word_frequency(words_with_entities)
    generate_word_cloud(word_freq, output_file)
