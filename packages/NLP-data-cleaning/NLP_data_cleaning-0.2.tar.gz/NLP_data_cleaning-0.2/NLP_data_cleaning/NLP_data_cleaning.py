import regex as re
import nltk
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from sklearn.base import BaseEstimator
from sklearn.base import TransformerMixin
import pandas as pd


class NLP_data_cleaning(BaseEstimator, TransformerMixin):
    nltk.download('stopwords')
    stop_words = set(stopwords.words('english'))

    def __init__(self):
        print("-----> init() called")

    def fit(self, X, y=None):
        print("-----> fit() called")
        return self

    def clean_text(self, X, y=None):
        words = re.sub("[X]", "", X)
        words = re.sub("[^a-zA-Z]"," ", words)
        text = words.lower().split()
        return " ".join(text)

    def transform(self, sentence_list, y=None):
        print("-----> transform() called")
        # cfpb_df_nlp = X[['consumer_complaint_narrative', 'issue', 'product', 'company_response_to_consumer', 'timely_response', 'company_public_response']]
        # cfpb_df_nlp.rename(columns={'consumer_complaint_narrative':'text'}, inplace=True)
        # cfpb_df_nlp['text_clear'] = cfpb_df_nlp['text'].apply(self.clean_text)
        # cfpb_df_nlp['text_clear'] = cfpb_df_nlp['text_clear'].apply(lambda x: ' '.join([word for word in x.split() if word not in (self.stop_words)]))
        
        cleaned_sentence_list = list(map(self.clean_text, sentence_list))
        cleaned_sentence_list = list(map(lambda x: ' '.join([word for word in x.split() if word not in (self.stop_words)]), cleaned_sentence_list))

        stemmed_data = []

        for txt in cleaned_sentence_list:
            txt_list = txt.split()
            stemmer = SnowballStemmer(language = 'english')
            txt_list_stemmed = [stemmer.stem(element) for element in txt_list]
            txt_stemmed = " ".join(txt_list_stemmed)
            stemmed_data.append(txt_stemmed)
    
        # cfpb_df_nlp['text_clean_stemmed'] = pd.Series(stemmed_data)

        # cfpb_df_nlp.drop(columns=['text', 'text_clear'], inplace = True)
        # cfpb_df_nlp.rename(columns={"text_clean_stemmed": "text"}, inplace = True)
        # cfpb_df_nlp.head()

        # cfpb_df_nlp = cfpb_df_nlp[['text', 'issue', 'product', 'company_response_to_consumer', 'company_public_response', 'timely_response']]

        return stemmed_data

