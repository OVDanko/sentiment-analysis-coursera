__author__ = 'olga_danko'


from nltk.corpus import stopwords
from pymystem3 import Mystem # лемматизация русских слов, можно установить через pip install
from string import punctuation
import re

from sklearn.pipeline import Pipeline

mystem = Mystem()
russian_stopwords = stopwords.words("russian")

# предобработчик текста
def text_filter(texts_to_filter):
    stop_words = stopwords.words('russian')
    filtered_texts = []
    for text in texts_to_filter:
        text= re.sub(r'[^\w\s]',' ',text) # убираем знаки пунктуации и прочие символы
        text = re.sub(' \d+', '', text) # убираем числа
        text= re.sub(r"\s+", ' ', text).strip() # убираем лишние пробелы
        tokens = mystem.lemmatize(text.lower()) # лемматизация
        tokens = [token for token in tokens if token not in stop_words and token != " " and token.strip() not in punctuation]
        text = " ".join(tokens)
        filtered_texts.append(text)
    return filtered_texts

# Pipeline модели
def text_classifier(vectorizer, classifier):
    return Pipeline(
            [("vectorizer", vectorizer),
            ("classifier", classifier)]
        )