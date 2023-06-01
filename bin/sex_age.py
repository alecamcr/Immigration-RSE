#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 24 23:18:10 2023

@author: alejandracamelocruz
"""

import argparse
import working_functions as wf
import pandas as pd
import seaborn as sns


def draw_bar_plot(data, years=6, sex=None, age=[10,20,30,40,50]):
    '''
    

    Parameters
    ----------
    data : TYPE
        DESCRIPTION.
    years : TYPE, optional
        DESCRIPTION. The default is 5.
    age : TYPE, optional
        DESCRIPTION. The default is [10,20,30,40,50].
    sex : TYPE, optional
        DESCRIPTION. The default is None.

    Returns
    -------
    bar_plot : TYPE
        DESCRIPTION.

    '''
    df = pd.read_csv(data)
    df_to_draw = wf.subset_years(df, years)
    df_to_draw = wf.subset_sex(df_to_draw, sex)
    df_to_draw = wf.subset_age(df_to_draw, age)

    title = wf.make_title(data)
    
    bar_plot = sns.catplot(data=df_to_draw, x='years', y='number', hue='sex', col='year',
                           col_wrap=3, kind='bar')
    bar_plot.fig.subplots_adjust(top=0.8)
    bar_plot.fig.suptitle(title)
    
    return bar_plot


def main(args):
    age = [int(age) for age in args.age_span]
    bar_plot = draw_bar_plot(args.infile, args.years, args.sex, age)
    bar_plot.savefig(args.outfile)

if __name__ == '__main__':
    data_path = wf.get_relative_path(
        'data/12711-0006_sex_age.csv')
    output_path = wf.get_relative_path(
        'results/immigrants_sex_age_external.png')
    
    parser = argparse.ArgumentParser(description = __doc__)
    parser.add_argument('--infile', type=str, nargs='*', 
                        default=data_path,
                        help='input files')
    parser.add_argument('--outfile', type=str, nargs='*',
                        default=output_path,
                        help='output file names')
    parser.add_argument('-age', '--age_span', nargs='+', default=[10,20,30,40,50],
                        help='list containing age span to be plotted')
    parser.add_argument('-y', '--years', type=int, default=6,
                        help='number of years to be plotted (max 21)')
    parser.add_argument('-s', '--sex', type=str,
                        help='sex to be plotted, all by default')
    
    args = parser.parse_args()
    main(args)