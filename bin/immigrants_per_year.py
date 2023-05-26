#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This function draws a line plot showing number of immigrants per n chosen year (by default 5)
of c chosen countries (by default 5) with biggest migration rate until 2021
"""

import argparse
import working_functions as funct
import pandas as pd
import seaborn as sns

def draw_line_plot(data, years=5, num_countries=5, country=None):
    df = pd.read_csv(data)
    df = df.loc[df['country'] != 'Total']
    df, selected_years = funct.subset_years(df, years, return_years=True)
    df_countries = funct.get_most_migrant_countries(df, num_countries, country)
        
    title = funct.make_title(data)
    line_plot = sns.relplot(data=df_countries, x='year', y='foreigners from foreign countries', hue='country',
                            kind='line')
    line_plot.fig.subplots_adjust(top=0.8)
    line_plot.fig.suptitle(title)
    line_plot.set(xticks=selected_years)
    
    return line_plot


def main(args):
    
    fig = draw_line_plot(args.data, args.years,
                   args.numcountries, args.country)
    fig.savefig(args.outfile)
    

if __name__ == '__main__':
    data_path = funct.get_relative_path(
        'data/12711-0008_external_migration.csv')
    output_path = funct.get_relative_path(
        'results/immigrants_per_year.png')
    
    parser = argparse.ArgumentParser(description=__doc__)
    
    parser.add_argument('data', type=str,
                        nargs='?', default=data_path)
    parser.add_argument('--outfile', type=str,
                        default=output_path,
                        help='optional output file name')
    parser.add_argument('-y', '--years', type=int, default=5,
                        help='number of years to be plotted (max 21)')
    parser.add_argument('-nc','--numcountries', type=int, default=5,
                        help='number of countries to be plotted\
                            (ordered by the n countries with most migrants)')
    parser.add_argument('-c','--country', type=str, default=None,
                        help='country to be plotted')
    
    args = parser.parse_args()
    main(args)
