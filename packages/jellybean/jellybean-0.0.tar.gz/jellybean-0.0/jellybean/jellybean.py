# Standard data science libraries
import pandas as pd
import numpy as np
from scipy import stats
from pathlib import Path
from cryptography.fernet import Fernet
import math
import re
import matplotlib.pyplot as plt

# NLP
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.model_selection import train_test_split as tts
import text_normalizer as tn
import warnings
from bs4 import BeautifulSoup
import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize.toktok import ToktokTokenizer
from contractions import contractions_dict
import re
import en_core_web_sm
import unicodedata
import cld2
from langdetect import detect
import contractions as ct
from tqdm import tqdm

# Used in class functions
#nlp = en_core_web_sm.load(parse=True, tag=True, entity=True)
tokenizer = ToktokTokenizer()
stopword_list = nltk.corpus.stopwords.words('english')

class jellybean():
    """ Addition class for performing addition by various quantities
    
    Attributes:
        i (int) starting integer
        q (float) however much you would like to add to i
        n (int) number of times to add q to i   
    """
        
    # Class constructor
    def __init__(self):
        pass

    # Get name of object
    def name_of_global_obj(self, x):
        return [objname for objname, oid in globals().items()
                if id(oid)==id(x)][0]
    
    # Assign to self
    def assign_self(self, obj):
        obj_name=name_of_global_obj(obj)
        eval(f'self.{obj_name} = {obj_name}')
    
    ###---Remove accented characters---###
    def remove_accented_chars(self, text):

        text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')
        return text
    
    ###---HTML Tags---###
    def strip_html_tags(self, text):
    
        soup = BeautifulSoup(text, "html.parser")
        stripped_text = re.sub(r'[\r|\n|\r\n|\t]+', '\n', soup.get_text())
        return stripped_text
    
    ###---Lemmatization---###
    #def lemmatize_text(self, text):
    #    
    #    text = nlp(text)
    #    text = ' '.join([word.lemma_ if word.lemma_ != '-PRON-' else word.text for word in text])
    #    return(text)
    
    ###---Removing Stopwords---###
    def remove_stopwords(self, text, is_lower_case=False):
    
        tokens = tokenizer.tokenize(text)
        tokens = [token.strip() for token in tokens]
        
        if is_lower_case:
            filtered_tokens = [token for token in tokens if token not in stopword_list]
        else:
            filtered_tokens = [token for token in tokens if token.lower() not in stopword_list]
            
        filtered_text = ' '.join(filtered_tokens)
        
        return filtered_text
    
    ###---Stemming---###
    def simple_stemmer(self, text):
    
        ps = nltk.porter.PorterStemmer()
        text = ' '.join([ps.stem(word) for word in text.split()])
        return text
    
    ###---Removing special characters---###
    def remove_special_characters(self, 
                                  text, 
                                  reg_w_dig=r'[^a-zA-z0-9\s]',
                                  reg_no_dig = r'[^a-zA-z\s]',
                                  remove_digits=False):
        pattern = reg if not remove_digits else reg_no_dig
        text = re.sub(pattern, '', text)
        return text
    
    ###---Case Conversion---###    
    def expand_contractions(self, text):
        return ct.fix(text)
    
    # Normalize function
    def normalize_corpus(self,
                         corpus, 
                         html_stripping=True,
                         contraction_expansion=True,
                         accented_char_removal=True,
                         text_lower_case=True,
                         #text_lemmatization=False,
                         special_char_removal=True,
                         stopword_removal=True,
                         remove_digits=True):
                         #detect_languages=True):
        
        self.initial_corpus = corpus
        
        normalized_corpus = []
        
        # normalize each document in the corpus
        for doc in tqdm(corpus):
                    
            if html_stripping:
                doc = self.strip_html_tags(doc)
            
            if accented_char_removal:
                doc = self.remove_accented_chars(doc)
                
            if contraction_expansion:
                doc = self.expand_contractions(doc)
                
            if text_lower_case:
                doc = doc.lower()
                
            # remove extra newlines
            doc = re.sub(r'[\r|\n|\r\n]+', ' ', doc)
            
            #if text_lemmatization:
            #    doc = self.lemmatize_text(doc)
                
            if special_char_removal:
                # Insert spaces between special characters to isolate them
                special_char_pattern = re.compile(r'([{.(-)!}])')
                doc = special_char_pattern.sub(" \\1", doc)
                doc = self.remove_special_characters(doc, remove_digits=remove_digits)
                    
            # remove extra whitespace and some other commonly occuring extra characters
            doc = re.sub(' +', ' ', doc)
            doc = re.sub('(?<=\[).*(?=\])|&#9; |\[|\] |` |[\\\] |[\^]', '', doc)
            
            if stopword_removal:
                doc = self.remove_stopwords(doc, is_lower_case=text_lower_case)
                
            # remove extra whitespace
            doc = re.sub(' +', ' ', doc)
            
            normalized_corpus.append(doc)
    
        self.norm_corpus = normalized_corpus
        
        return normalized_corpus
    
    # Clean data frame
    def clean_df(self, df, corpus_column, word_cutoff=3):
        
        # Perform normalize function
        df['norm_corpus'] = self.normalize_corpus(df[corpus_column])
        
        # Remove documents without enough words (determined by word_cutoff)
        df = df[[len(re.split(' ', a)) > word_cutoff for a in df['norm_corpus']]]
        
        # Remove non english documents
        df['Language'] = [cld2.detect(doc)[2][0][0] for doc in df.norm_corpus]
        df = df[df.Language=='ENGLISH']
        df.drop(['Language'], axis=1, inplace=True)
        
        return(df)
    
    # TVT
    def tvt(self, 
            df=None, 
            corpus_column=None, 
            word_cutoff=None, 
            target_column=None, 
            stratify=False,
            normalize=False,
            random_state=273):
        
        if normalize:
            
            norm_df = self.clean_df(df, corpus_column, word_cutoff)
            X = norm_df.drop(columns=[target_column])
            y = norm_df[target_column]
            X_train, X_test, y_train, y_test = tts(X, y, test_size=0.2, random_state=random_state)
            
            # Assign these sets to self
            self.X_train=X_train
            self.X_test=X_test
            self.y_train=y_train
            self.y_test=y_test
            
            return X_train, X_test, y_train, y_test
        
        else:
            
            X = df.drop(columns=[target_column])
            y = df[target_column]
            X_train, X_test, y_train, y_test = tts(X, y, test_size=0.2)
            
            # Assign these sets to self
            self.X_train=X_train
            self.X_test=X_test
            self.y_train=y_train
            self.y_test=y_test
            
            return X_train, X_test, y_train, y_test

    # Create BOW features
    def create_bow_features(self, X_train, X_test):
        cv = CountVectorizer(binary=False, min_df=0.0, max_df=1.0)
        self.cv_tr_X = cv.fit_transform(X_train)
        self.cv_te_X = cv.transform(X_test)
        
        return self.cv_tr_X, self.cv_te_X
        
    # Create Tf-idf features
    def create_tfidf_features(self, X_train, X_test):
        tv = TfidfVectorizer(use_idf=True, min_df=0.0, max_df=1.0)
        self.tv_tr_X = tv.fit_transform(X_train)
        self.tv_te_X = tv.transform(X_test)
        
        return self.tv_tr_X, self.tv_te_X
    