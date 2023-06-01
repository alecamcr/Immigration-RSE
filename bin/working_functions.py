#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
returns relative path from project root directory
"""

import os
import re
import pandas as pd


def get_most_migrant_countries(df, num_countries, country=False):
    '''


    Parameters
    ----------
    df : TYPE
        DESCRIPTION.
    num_countries : TYPE
        DESCRIPTION.
    country : TYPE, optional
        DESCRIPTION. The default is False.

    Returns
    -------
    df_countries : TYPE
        DESCRIPTION.

    '''
    if 'country' in df:
        if country:
            df_countries = df.loc[df['country'] == country]
        else:
            most_migrant = df.loc[df['year'] == 2021]\
                .sort_values('foreigners from foreign countries', 
                             ascending=False).head(num_countries)
            most_migrant = list(most_migrant.iloc[:, 1])
            df_countries = df.loc[df['country'].isin(most_migrant)]  
            
    if 'origin' in df:
            most_migrant = df.loc[(df['year'] == 2021) & (df['origin'] == 'Insgesamt')
                                  & (df['destination'] != 'Insgesamt')]\
                                    .sort_values('total foreigners', 
                             ascending=False).head(num_countries)
            most_migrant = list(most_migrant.iloc[:, 2])
            df_countries = df.loc[df['destination'].isin(most_migrant)]  
 

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
    df_years = df.loc[df['year'].isin(selected_years)]
    
    if return_years:
        return df_years, selected_years
    else:
        return df_years


def subset_sex(df, sex):
    '''
    

    Parameters
    ----------
    df : TYPE
        DESCRIPTION.
    sex : TYPE
        DESCRIPTION.

    Returns
    -------
    df : TYPE
        DESCRIPTION.

    '''
    male = (sex == 'male')
    female = (sex == 'female')
    if 'years' in df:
        df_sex = df[['year','years','foreigners male arrivals', 
                     'foreigners female arrivals']]
    else:
        df_sex = df[['year','origin', 'destination', 'foreigners male arrivals', 
                     'foreigners female arrivals']]
    df_sex = df_sex.rename(columns={'foreigners male arrivals':'male', 
                                    'foreigners female arrivals':'female'})
    if male:
        df_sex = df_sex.drop('female', axis=1)
    if female:
        df_sex = df_sex.drop('male', axis=1)
        
    columns = [column for column in df_sex if column not in ['male', 'female']]
    
    df_melted = df_sex.melt(id_vars=columns, var_name= 'sex', 
                                value_name='number')
        
    return df_melted


def subset_age(df, age):
    '''
    

    Parameters
    ----------
    df : TYPE
        DESCRIPTION.
    age : TYPE
        DESCRIPTION.

    Returns
    -------
    df : TYPE
        DESCRIPTION.

    '''
    
    df['years'] = df.years.str.replace(r'([a-z]*)' , '')
    df['years'] = pd.to_numeric(df['years'], errors='coerce')
    df_age = df.loc[df['years'].isin(age)]
    
    return df_age

def fedcountry_to_int(data, column=None, return_mapping=False):
    new_df = data
    to_int = {'Schleswig-Holstein': 0, 'Hamburg': 1, 'Niedersachsen': 2, 'Bremen': 3,
              'Nordrhein-Westfalen': 4, 'Hessen': 5, 'Rheinland-Pfalz': 6,
              'Baden-Wurttemberg': 7, 'Bayern': 8, 'Saarland': 9, 'Berlin': 10,
              'Brandenburg': 11, 'Mecklenburg-Vorpommern': 12, 'Sachsen': 13,
             'Sachsen-Anhalt': 14, 'Thuringen': 15, 'Insgesamt': 16}
    
    if column:
        new_df[column] = new_df.origin.map(to_int)
    else:
        new_df['origin'] = new_df.origin.map(to_int)
        new_df['destination'] = new_df.destination.map(to_int)
    
    if return_mapping:
        return new_df, to_int
    else: 
        return new_df

def fedcountry_to_str(data, column=None, return_mapping=False):
    new_df = data
    to_str = {0: 'Schleswig-Holstein', 1: 'Hamburg', 2: 'Niedersachsen', 3: 'Bremen',
              4: 'Nordrhein-Westfalen', 5: 'Hessen', 6: 'Rheinland-Pfalz',
              7: 'Baden-Wurttemberg', 8: 'Bayern', 9: 'Saarland', 10: 'Berlin',
              11: 'Brandenburg', 12: 'Mecklenburg-Vorpommern', 13: 'Sachsen',
              14: 'Sachsen-Anhalt', 15: 'Thuringen', 16: 'Insgesamt'}
    if column:
        new_df[column] = new_df.origin.map(to_str)
    else:
        new_df['origin'] = new_df.origin.map(to_str)
        new_df['destination'] = new_df.destination.map(to_str)
    
    if return_mapping:
        return new_df, to_str
    else: 
        return new_df


def make_title(name):
    '''
    

    Parameters
    ----------
    name : TYPE
        DESCRIPTION.

    Returns
    -------
    title : TYPE
        DESCRIPTION.

    '''
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