#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File containing important working functions for workflow

"""

import os
import re
import pandas as pd


def get_most_migrant_countries(df, num_countries: int, country=False):
    '''
    This function subset the n countries with most migration
    in the dataset specified by numcountries. If country is given,
    it'll subset only that country. It works with world and federal countries

    Parameters
    ----------
    df : pandas dataframe
        dataframe to subset.
    num_countries : int
        number of countries to subset.
    country : TYPE, optional
        DESCRIPTION. The default is False.

    Returns
    -------
    df_countries : pandas dataframe
        subsetted dataframe.

    '''
    if country:
        df_countries = df.loc[df['country'] == country]

    elif 'country' in df:
        most_migrant = df.loc[df['year'] == 2021]\
            .sort_values('foreigners from foreign countries',
                         ascending=False).head(num_countries)
        most_migrant = list(most_migrant.iloc[:, 1])
        df_countries = df.loc[df['country'].isin(most_migrant)]

    elif 'origin' in df:
        most_migrant = df.loc[(df['year'] == 2021)
                              & (df['origin'] == 'Insgesamt')
                              & (df['destination'] != 'Insgesamt')]\
            .sort_values('total foreigners',
                         ascending=False).head(num_countries)
        most_migrant = list(most_migrant.iloc[:, 2])
        df_countries = df.loc[df['destination'].isin(most_migrant)]

    return df_countries


def subset_years(df, years: int, return_years=False):
    '''
    This function subset the n past years from 2021 in the dataset specified
    by years. If return_years is set to True,
    it'll return a list with the years.

    Parameters
    ----------
    df : pandas dataframe
        Dataframe to subset.
    years : int
        Number of years to subset.
    return_true: bool, optional
        Returns list with subsetted years if True. False by default

    Returns
    -------
    df : pandas dataframe
        subsetted dataframe.
    selected_years : list
        list with subsetted years.

    '''
    end_year = 2021-years
    selected_years = [year for year in range(2021, end_year, -1)]
    df_years = df.loc[df['year'].isin(selected_years)]

    if return_years:

        return df_years, selected_years
    else:

        return df_years


def subset_sex(df, sex=None):
    '''
    This function subset sex if given. If not, it'll only melt the dataframe
    by sex for further manipulation

    Parameters
    ----------
    df : pandas dataframe
        Dataframe to subset.
    sex : str, optional
        male or female accepted. None by default

    Returns
    -------
    df : pandas dataframe
        subsetted dataframe.

    '''
    columns = [column for column in df]
    df_sex = df[columns]
    df_sex = df_sex.rename(columns={'foreigners male arrivals': 'male',
                                    'foreigners female arrivals': 'female'})

    if sex:
        male = (sex == 'male')
        female = (sex == 'female')
        if male:
            df_sex = df_sex.drop('female', axis=1)
        if female:
            df_sex = df_sex.drop('male', axis=1)

    columns = [column for column in df_sex if column not in ['male', 'female']]

    df_melted = df_sex.melt(id_vars=columns, var_name='sex',
                            value_name='number')

    return df_melted


def subset_age(df, age: list):
    '''
    This function subset age in given data set. Age must be given
    in list format specifying ages that want to be submitted

    Parameters
    ----------
    df : pandas dataframe
        Dataframe to subset.
    age : list
        List with desired ages

    Returns
    -------
    df : TYPE
        DESCRIPTION.

    '''

    df['years'] = df.years.str.replace(r'([a-z]*)', '')
    df['years'] = pd.to_numeric(df['years'], errors='coerce')
    df_age = df.loc[df['years'].isin(age)]

    return df_age


def fedcountry_to_int(data, column=None, return_mapping=False):
    '''
    This function map federal countries into integers.
    If column is chosen, only that column will be mapped.
    Otherwise, both columns containing names of federal countries are mapped

    Parameters
    ----------
    data : pandas dataframe
        pandas dataframe to subset.
    column : str, optional
        If given, origin or destination accepted. Specifies column to be
        mapped. The default is None.
    return_mapping : bool, optional
        If true, mapping dictionary is returned. The default is False.

    Returns
    -------
    pandas dataframe, dict
        returns subsetted dataframe.
        If return_mapping set to True, returns dict containing
        the mapping

    '''
    new_df = data
    to_int = {'Schleswig-Holstein': 0, 'Hamburg': 1, 'Niedersachsen': 2,
              'Bremen': 3, 'Nordrhein-Westfalen': 4, 'Hessen': 5,
              'Rheinland-Pfalz': 6, 'Baden-Wurttemberg': 7, 'Bayern': 8,
              'Saarland': 9, 'Berlin': 10, 'Brandenburg': 11,
              'Mecklenburg-Vorpommern': 12, 'Sachsen': 13,
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


def make_title(name: str):
    '''
    This function create san appropriate title for a plot from data file path

    Parameters
    ----------
    name : str
        data file path.

    Returns
    -------
    title : str
        Appropriate title from file path.

    '''
    title = name
    title = re.sub(r'.*/', '', title)
    title = title.replace('_', ' ').replace('.csv', '')

    return title


def get_relative_path(file_path: str):
    '''
    This function creates a relative path for working files

    Parameters
    ----------
    file_path : str
        absolute path of file with parent directory.

    Returns
    -------
    full_path : str
        relative path to root directory.

    '''
    absolute_path = os.path.dirname(__file__)
    relative_path = file_path
    full_path = os.path.join(absolute_path, '..', relative_path)

    return full_path
