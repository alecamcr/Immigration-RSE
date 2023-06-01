#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 30 17:56:26 2023

@author: alejandracamelocruz
"""

import argparse
import working_functions as wf
import pandas as pd
import seaborn as sns

def draw_scatter_plot(data, years=6, numcountries=5, country=None, sex=None):
    df = pd.read_csv(data)
    df_to_draw = wf.get_most_migrant_countries(df, numcountries, country)
    df_to_draw = wf.subset_years(df_to_draw, years)
    df_to_draw = wf.subset_sex(df_to_draw, sex)
    df_to_draw, mapping = wf.fedcountry_to_int(df_to_draw, column = 'origin',
                                               return_mapping=True)
    
    title = wf.make_title(data)
    scatter_plot = sns.relplot(data=df_to_draw, x='origin', y='number', hue='destination',
                           col='year', row='sex', kind='scatter')
    scatter_plot.fig.subplots_adjust(top=0.8)
    indices = [index for index in mapping.values()]
    names = [name for name in mapping]
    for ax in scatter_plot.axes.flat:
        ax.set_xticks(ticks=indices)
        ax.set_xticklabels(fontsize=8, rotation=90, labels=names)
    
    scatter_plot.fig.suptitle(title)
    
    return scatter_plot
    


def main(args):
    scatter_plot = draw_scatter_plot(args.infile, args.years, args.numcountries,
                      args.country, args.sex)
    scatter_plot.savefig(args.outfile)

if __name__ == '__main__':
    data_path = wf.get_relative_path(
        'data/12711-0022_internal_migration.csv')
    output_path = wf.get_relative_path(
        'results/scatter_internal_migration.png')
    
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument('--infile', type=str,
                        nargs='?', default=data_path)
    parser.add_argument('--outfile', type=str,
                        default=output_path,
                        help='optional output file name. If both types are plotted\
                             first name for line plot and second name for bar plot')
    parser.add_argument('-y', '--years', type=int, default=6,
                        help='number of years to be plotted (max 21)')
    parser.add_argument('-nc','--numcountries', type=int, default=5,
                        help='number of countries to be plotted\
                            (ordered by the n countries with most migrants)')
    parser.add_argument('-c','--country', type=str, default=None,
                        help='country to be plotted')
    parser.add_argument('-s', '--sex', type=str,
                        help='sex to be plotted, all by default')
    
    args = parser.parse_args()
    main(args)