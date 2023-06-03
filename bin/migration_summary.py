#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This function draws line, bar and scatter plots showing number of immigrants
per n chosen year (by default 6) of m chosen world and federal countries
(by default 5), for given sex and age (by default 10, 20, 30, 40 and 50)
with biggest migration rate until 2021. If country is given
only that country will be plotted. infile and outfile names are given
by default but can be changed without flag. This function is intended
to provide a summary of important features of migration for further analysis
"""

import argparse
import sex_age
import external_migration
import internal_migration
import working_functions as wf


def main(args):
    infiles = [file for file in args.infiles]
    outfiles = [file for file in args.outfiles]
    age = [int(age) for age in args.age_span]

    bar_sex_age = sex_age.draw_bar_plot(infiles[0], args.years,
                                        args.sex, age)
    bar_sex_age.savefig(outfiles[0])

    line_external = external_migration.draw_line_plot(infiles[1], args.years,
                                                      args.numcountries,
                                                      args.country)
    line_external.savefig(outfiles[1])

    bar_external = external_migration.draw_bar_plot(infiles[1], args.years,
                                                    args.numcountries,
                                                    args.country)
    bar_external.savefig(outfiles[2])

    scatter_internal = internal_migration.draw_scatter_plot(infiles[2],
                                                            args.years,
                                                            args.numcountries,
                                                            args.federalcountry,
                                                            args.sex)
    scatter_internal.savefig(outfiles[3])


if __name__ == '__main__':

    sex_age_data = wf.get_relative_path(
        'data/12711-0006_sex_age.csv')
    sex_age_output = wf.get_relative_path(
        'results/immigrants_sex_age_external.png')

    external_data = wf.get_relative_path(
        'data/12711-0008_external_migration.csv')
    external_line_output = wf.get_relative_path(
        'results/line_immigrants_per_year.png')
    external_bar_output = wf.get_relative_path(
        'results/bar_immigrants_per_year.png')

    internal_data = wf.get_relative_path(
        'data/12711-0022_internal_migration.csv')
    internal_output = wf.get_relative_path(
        'results/scatter_internal_migration.png')

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('infiles', type=str, nargs='*',
                        default=[sex_age_data, external_data,
                                 internal_data])
    parser.add_argument('outfiles', type=str, nargs='*',
                        default=[sex_age_output, external_line_output,
                                 external_bar_output, internal_output],
                        help='name of output files. In order they have to be ')
    parser.add_argument('-y', '--years', type=int, default=6,
                        help='number of years to be plotted (max 21)')
    parser.add_argument('-nc', '--numcountries', type=int, default=5,
                        help='number of countries to be plotted\
                            (ordered by the n countries with most migrants)')
    parser.add_argument('-c', '--country', type=str, default=None,
                        help='country to be plotted')
    parser.add_argument('-fc', '--federalcountry', type=str, default=None,
                        help='country to be plotted')
    parser.add_argument('-age', '--age_span', nargs='*',
                        default=[10, 20, 30, 40, 50],
                        help='list containing age span to be plotted')
    parser.add_argument('-s', '--sex', type=str,
                        help='sex to be plotted, all by default')

    args = parser.parse_args()
    main(args)
