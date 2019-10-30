#!/usr/bin/env python
# coding: utf-8

# In[1]:


import FieldExt as field_extraction
import JobLib as lib

import inspect
import sys
import logging
import os
import re
import subprocess
import pandas as pd
import pandas
import yaml
import spacy

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

def main():
    """
    Main function documentation template
    :return: None
    :rtype: None
    """
    logging.getLogger().setLevel(logging.INFO)

    # Extract data from upstream.
    observations = pd.read_csv("DescriptionsTest.csv")

    # Spacy: Spacy NLP
    nlp = spacy.load('en')

    # Transform data to have appropriate fields
    observations, nlp = transform(observations, nlp)

    # Load data for downstream consumption
    load(observations, nlp)

    pass

def transform(observations, nlp):
    # TODO Docstring
    logging.info('Begin transform')

    # Extract skills
    observations = field_extraction.data_cleaning(observations)
    #print(observations.columns)
    observations = field_extraction.extract_fields(observations)
    #print(observations.columns)
    # Archive schema and return
    lib.archive_dataset_schemas('transform', locals(), globals())
    logging.info('End transform')
    return observations, nlp

def load(observations, nlp):
    logging.info('Begin load')
    output_path = os.path.join(lib.get_conf('summary_output_directory'), 'JOB_DESCRIPTION_summary.csv')

    logging.info('Results being output to {}'.format(output_path))
    print('Results output to {}'.format(output_path))

    observations.to_csv(path_or_buf=output_path, index_label='index')
    logging.info('End transform')
    pass

# Main section
if __name__ == '__main__':
    main()

