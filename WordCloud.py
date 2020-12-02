import streamlit as st
from wordcloud import WordCloud, STOPWORDS
import numpy as np
import io
from matplotlib import pyplot as plt
from collections import Counter

def wordcloud_gen(string_data):
    text_list = string_data.split('\n')
    # removing nulls
    text_list = [x.strip() for x in text_list]
    text_list = [x for x in text_list if x]

    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~“”‘’—£'''
    punc_dict = dict()
    for _ in punctuations:
        punc_dict[_] = ord(_)
    no_pun_dict = dict(zip(punc_dict.values(), [None] * len(punc_dict)))

    no_pun = [x.translate(no_pun_dict) for x in text_list]
    no_pun = [x.strip() for x in no_pun]
    no_pun_str = ' '.join(no_pun)

    uninteresting_words = ["the", "a", "to", "if", "is", "it", "of", "and", "or", "an", "as", "i", "me", "my",
                           "we", "our", "ours", "you", "your", "yours", "he", "she", "him", "his", "her", "hers",
                           "its", "they", "them", "their", "what", "which", "who", "whom", "this", "that", "am",
                           "are", "was", "were", "be", "been", "being", "have", "has", "had", "do", "does", "did",
                           "but", "at", "by", "with", "from", "here", "when", "where", "how","all", "any", "both",
                           "each", "few", "more", "some", "such", "no", "nor", "too", "very", "can", "will", "just",
                           'for', 'in', 'said']

    splitted = no_pun_str.split()
    spl = [x.lower() for x in splitted]
    final = [word for word in spl if word not in uninteresting_words]
    final_str = ' '.join(final)

    final_str = final_str.strip()
    final_list = final_str.split()
    freq = Counter(final_list)
    return freq

st.title('WordCloud Generator')
st.write('A simple app to generate wordcloud from txt files based on the frequencies of words in them.')

st.sidebar.header('File Uploader')
uploaded_file = st.sidebar.file_uploader('Upload a file', type=['txt'])
color = st.sidebar.beta_color_picker('Select background color for wordcloud', '#000000')

if uploaded_file:
    st.sidebar.success(f'Uploaded **{uploaded_file.name}**!')
    file_contents = uploaded_file.read()
    stringio = io.StringIO(file_contents.decode('utf-8'))
    string_data = stringio.read()

    freq = wordcloud_gen(string_data)
    if freq:
            st.write(f'### WordCloud of {uploaded_file.name.split(".")[0]}')
            cloud = WordCloud(width=1800, height=1400,
                              background_color=color,
                              stopwords=STOPWORDS).generate_from_frequencies(freq)
            cloud = cloud.to_array()
            fig = plt.figure(figsize=(15, 15), facecolor='w')
            plt.imshow(cloud, interpolation='nearest')
            plt.axis('off')
            st.pyplot(fig)
            st.sidebar.info('The generated image can be downloaded by using the **save image as...** option in the '
                            'menu')






