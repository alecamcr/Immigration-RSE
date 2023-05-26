#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 24 23:18:10 2023

@author: alejandracamelocruz
"""

import argparse
import working_functions as funct
import pandas as pd
import seaborn as sns

def draw_bar_plot(data, years=5, age=[10,20,30,40,50], sex=None):
    df = pd.read_csv(data)
    df = funct.subset_years(df, years)
    df = funct.subset_sex(df, sex)
    df = funct.subset_age(df, age)

    title = funct.make_title(data)
    
    bar_plot = sns.catplot(data=df, x='years', y='number', hue='sex', col='year',
                           kind='bar')
    bar_plot.fig.subplots_adjust(top=0.8)
    bar_plot.fig.suptitle(title)
    
    return bar_plot
    
    
def draw_bar_plotgeo_plot(data, years=5, age=[20,40], sex=None):
    pass

def main(args):
    for i in range(len(args.infiles)):
        bar_plot = draw_bar_plot(args.infiles[i])
        bar_plot.savefig(args.outfiles[i])

if __name__ == '__main__':
    external_data_path = funct.get_relative_path(
        'data/12711-0006_sex_age_external.csv')
    internal_data_path = funct.get_relative_path(
        'data/12711-0002_sex_age_internal.csv')
    external_output_path = funct.get_relative_path(
        'results/immigrants_sex_age_external.png')
    internal_output_path = funct.get_relative_path(
        'results/immigrants_sex_age_internal.png')
    
    parser = argparse.ArgumentParser(description = __doc__)
    parser.add_argument('infiles', type=str, nargs='*', 
                        default=[external_data_path, internal_data_path],
                        help='input files')
    parser.add_argument('outfiles', type=str, nargs='*',
                        default=[external_output_path, internal_output_path],
                        help='output file names')
    parser.add_argument('-age', '--age_span', type=list,
                        default=[10,20,30,40,50],
                        help='list containing age span to be plotted')
    parser.add_argument('-y', '--years', type=int, default=5,
                        help='number of years to be plotted (max 21)')
    
    args = parser.parse_args()
    test = main(args)