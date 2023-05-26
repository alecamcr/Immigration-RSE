#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
returns relative path from project root directory
"""

import os
import re
import pandas as pd

def get_most_migrant_countries(df, num_countries, country=False):
    if country:
        df_countries = df.loc[df['country'] == country]
    else:
        most_migrant = df.loc[df['year'] == 2021]\
            .sort_values('foreigners from foreign countries',
                         ascending=False).head(num_countries)
        most_migrant = list(most_migrant.iloc[:,1])
        df_countries = df.loc[df['country'].isin(most_migrant)]
    
    return df_countries

def subset_years(df, years, return_years=False):
    '''
    

    Parameters
    ----------
    data : pandas dataframe
        DESCRIPTION.
    years : int
        DESCRIPTION.

    Returns
    -------
    df : pandas dataframe
        DESCRIPTION.
    selected_years : list
        DESCRIPTION.

    '''
    end_year = 2021-years
    selected_years = [year for year in range(2021,end_year,-1)]
    df = df.loc[df['year'].isin(selected_years)]
    
    if return_years:
        return df, selected_years
    else:
        return df

def subset_sex(df, sex):
    male = (sex == 'male')
    female = (sex == 'female')
    df = df[['year','years','foreigners male arrivals', 'foreigners female arrivals']]
    df = df.rename(columns={'foreigners male arrivals':'male', 'foreigners female arrivals':'female'})
    if male:
        df = df.drop('female', axis=1)
    if female:
        df = df.drop('male', axis=1)
        
    return df

def subset_age(df, age):
    df['years'] = df.years.str.replace(r'([a-z]*)' , '')
    df['years'] = pd.to_numeric(df['years'], errors='coerce')
    df = df.loc[df['years'].isin(age)]
    df = df.melt(id_vars=['year', 'years'], var_name= 'sex', value_name='number')
    
    return df

def make_title(name):
    title = name
    title = re.sub(r'.*/', '', title)
    title = title.replace('_', ' ').replace('.csv', '')
    
    return title

def get_relative_path(file_path):
    '''

    Parameters
    ----------
    file_path : str
        absolute path of file with parent directory.

    Returns
    -------
    relative path to root directory.

    '''
    absolute_path = os.path.dirname(__file__)
    relative_path = file_path
    full_path = os.path.join(absolute_path, '..', relative_path)
    
    return full_path