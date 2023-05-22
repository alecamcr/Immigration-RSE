#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This function draws a line plot showing number of immigrants per n chosen year (by default 5)
of c chosen countries (by default 5) with biggest migration rate until 2021
"""

import argparse
import working_paths as pth
import pandas as pd
import seaborn as sns

def main(args):
    df = pd.read_csv(args.data)
    df = df.loc[df['country'] != 'Total']
    
    end_year = 2021-args.years
    selected_years = [year for year in range(2021,end_year,-1)]
    df = df.loc[df['year'].isin(selected_years)]
    
    if args.country:
        df_countries = df.loc[df['country'] == args.country]
    else:
        most_migrant = df.loc[df['year'] == 2021]\
            .sort_values('foreigners from foreign countries',
                         ascending=False).head(args.numcountries)
        most_migrant = list(most_migrant.iloc[:,1])
        df_countries = df.loc[df['country'].isin(most_migrant)]
        
    line_plot = sns.lineplot(data=df_countries, x='year',\
                 y='foreigners from foreign countries', hue='country')
    line_plot.set(xticks=selected_years)
    
    fig = line_plot.get_figure()
    fig.savefig(args.outfile)
    

if __name__ == '__main__':
    data_path = pth.get_relative_path(
        'data/12711-0008-Migration between Germany and foreign countries.csv')
    output_path = pth.get_relative_path(
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
