#!/usr/bin/env python
# coding: utf-8

# In[1]:


import logging
import string
import nltk
from nltk.tokenize import word_tokenize
from gensim.utils import simple_preprocess

import JobLib as lib

def extract_fields(df):
    for extractor, items_of_interest in lib.get_conf('extractors').items():
        df[extractor] = df['Job Description Cleaned'].apply(lambda x: extract_skills(x, extractor, items_of_interest))
    return df


def extract_skills(jobDescriptionText, extractor, items_of_interest):
    potential_skills_dict = dict()
    matched_skills = set()

    # TODO This skill input formatting could happen once per run, instead of once per observation.
    for skill_input in items_of_interest:

        # Format list inputs
        if type(skill_input) is list and len(skill_input) >= 1:
            potential_skills_dict[skill_input[0]] = skill_input

        # Format string inputs
        elif type(skill_input) is str:
            potential_skills_dict[skill_input] = [skill_input]
        else:
            logging.warn('Unknown skill listing type: {}. Please format as either a single string or a list of strings'
                         ''.format(skill_input))

    for (skill_name, skill_alias_list) in potential_skills_dict.items():

        skill_matches = 0
        # Iterate through aliases
        for skill_alias in skill_alias_list:
            # Add the number of matches for each alias
            skill_matches += lib.term_count(jobDescriptionText, skill_alias.lower())

        # If at least one alias is found, add skill name to set of skills
        if skill_matches > 0:
            matched_skills.add(skill_name)

    return matched_skills

def remove_punctuation(text):
    text = text.replace(r"\n", " ")
    text = text.replace('/', ' ')
    for punctuation in string.punctuation:
        text = text.replace(punctuation, '')
    return text

def remove_stop_words(text):
    stopwords = set(nltk.corpus.stopwords.words('english'))
    try:
        word_tokens = word_tokenize(text)
        filtered_sentence = [w for w in word_tokens if not w in stopwords]
        return ' '.join(filtered_sentence)
    except:
        print(text.values)
        sys.exit(1)

def lowercase_all(text):
    text_lower = text.lower()
    return text_lower

def data_cleaning(df):
    df['Job Description Cleaned'] = df['Job Description'].apply(remove_punctuation)
    df['Job Description Cleaned'] = df['Job Description Cleaned'].apply(lowercase_all)
    df['Job Description Cleaned'] = df['Job Description Cleaned'].apply(remove_stop_words)
    return df
    

