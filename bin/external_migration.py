#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This function draws line and bar plots showing number of immigrants
per n chosen year (by default 6) of chosen countries (by default 5)
with biggest migration rate until 2021. If country is given
only that country will be plotted. infile and outfile names are given
by default but can be changed without flag.
If optional argument kind is specified, only bar plot or only line plot
will be plotted

Copyright (C) 2023 Alejandra Camelo Cruz

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

contact email: camelocruz@uni-potsdam.de

"""

import argparse
import working_functions as wf
import pandas as pd
import seaborn as sns


def draw_line_plot(data, years=6, numcountries=5, country=None):
    '''
    This function draws a line plot showing number of immigrants
    per n chosen year (by default 6) of chosen countries (by default 5)
    with biggest migration rate until 2021. If country is given
    only that country will be plotted

    Parameters
    ----------
    data : pandas dataframe
        dataframe to plot.
    years : int, optional
        number of years to subset. The default is 5.
    num_countries : int, optional
        number of countries to subset. The default is 5.
    country : str, optional
        name of country to subset. The default is None.

    Returns
    -------
    line_plot : seaborn FacetGrid
        line plot with most migrant country visualization.

    '''
    df = pd.read_csv(data)
    df_to_draw = df.loc[df['country'] != 'Total']
    df_to_draw, selected_years = wf.subset_years(df_to_draw, years,
                                                 return_years=True)
    df_to_draw = wf.get_most_migrant_countries(df_to_draw,
                                               numcountries, country)

    title = wf.make_title(data)
    line_plot = sns.relplot(data=df_to_draw, x='year',
                            y='foreigners from foreign countries',
                            hue='country', kind='line')
    line_plot.fig.subplots_adjust(top=0.8)
    line_plot.fig.suptitle(title)
    for ax in line_plot.axes.flat:
        ax.set_xticks(ticks=selected_years)
        ax.set_xticklabels(fontsize=8, rotation=90, labels=selected_years)

    return line_plot


def draw_bar_plot(data, years=6, num_countries=5, country=None):
    '''
    This function draws a bar plot showing number of immigrants
    per n chosen year (by default 6) of chosen countries (by default 5)
    with biggest migration rate until 2021. If country is given
    only that country will be plotted

    Parameters
    ----------
    data : pandas dataframe
        dataframe to plot.
    years : int, optional
        number of years to subset. The default is 6.
    num_countries : TYPE, optional
        number of countries to subset. The default is 5.
    country : TYPE, optional
        name of country to subset. The default is None.

    Returns
    -------
    bar_plot : seaborn FacetGrid
        line plot with most migrant country visualization.

    '''
    df = pd.read_csv(data)
    df_to_draw = df.loc[df['country'] != 'Total']
    df_to_draw, selected_years = wf.subset_years(df_to_draw, years,
                                                 return_years=True)
    df_to_draw = wf.get_most_migrant_countries(df_to_draw,
                                               num_countries, country)

    title = wf.make_title(data)
    bar_plot = sns.catplot(data=df_to_draw, x='country',
                           y='foreigners from foreign countries', col='year',
                           col_wrap=3, kind='bar')

    bar_plot.fig.subplots_adjust(top=0.8)
    bar_plot.fig.suptitle(title)
    countries = {count: value for count, value
                 in enumerate(df_to_draw['country'].unique())}
    indices = [index for index in countries]
    names = [name for name in countries.values()]
    for ax in bar_plot.axes.flat:
        ax.set_xticks(ticks=indices)
        ax.set_xticklabels(fontsize=8, rotation=90, labels=names)

    return bar_plot


def main(args):
    outfiles = [file for file in args.outfile]
    if args.kind:
        line = (args.kind == 'line')
        bar = (args.kind == 'bar')
        if line:
            fig = draw_line_plot(args.infile, args.years,
                                 args.numcountries, args.country)
            fig.savefig(outfiles[0])
        if bar:
            fig = draw_bar_plot(args.infile, args.years,
                                args.numcountries, args.country)
            fig.savefig(outfiles[0])
    else:
        line = draw_line_plot(args.infile, args.years,
                              args.numcountries, args.country)
        line.savefig(outfiles[0])

        bar = draw_bar_plot(args.infile, args.years,
                            args.numcountries, args.country)
        bar.savefig(outfiles[1])


if __name__ == '__main__':
    data_path = wf.get_relative_path(
        'data/12711-0008_external_migration.csv')
    line_output_path = wf.get_relative_path(
        'results/line_immigrants_per_year.png')
    bar_output_path = wf.get_relative_path(
        'results/bar_immigrants_per_year.png')

    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument('outfile', type=str,
                        nargs='*', default=[line_output_path, bar_output_path],
                        help='optional output file name.\
                             If both types are plotted\
                             first name for line plot\
                             and second name for bar plot')
    parser.add_argument('--infile', type=str,
                        nargs='*', default=data_path)
    parser.add_argument('-k', '--kind', type=str,
                        help='kind of plot to present data. line or bar\
                             by default both are plotted')
    parser.add_argument('-y', '--years', type=int, default=6,
                        help='number of years to be plotted (max 21)')
    parser.add_argument('-nc', '--numcountries', type=int, default=5,
                        help='number of countries to be plotted\
                            (ordered by the n countries with most migrants)')
    parser.add_argument('-c', '--country', type=str, default=None,
                        help='country to be plotted')

    args = parser.parse_args()
    main(args)
