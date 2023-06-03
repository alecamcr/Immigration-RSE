# Project overview

## Goal

This project aims at summarizing important factors of [immigration](https://en.wikipedia.org/wiki/Immigration)  in Germany, such as: number of immigrants, origin countries, sex, age, and concentration and movement between Bundesländer. This summary become relevant for further analysis about public policies and future research about:

- Public policies addressing specific immigrant groups
- linguistic integration in general and in each of the federal countries
- General linguistic public policies and preservation of heritage languages
- Needed future implementations in order to facilitate integration

## Project research questions

1. Total number of immigrants reported per year, differentiating countries
2. Distribution of sex and age of children reported per year
3. Distribution of sex and age in scholarization ages reported per year
4. Distribution of sex and age of older persons ages reported per year
5. Movement of immigrants, differentiating sex, between Bundesländer 

## Data sets

For this project three data sets with data about migration in Germany until 2021 were used. The data sets can be recovered in the page of the database of the Federal Statistical Office of Germany [destatis](https://www-genesis.destatis.de/genesis/online/data?operation=sprachwechsel&language=en) under **1 territory, population, labour market, elections**; **12 population**; **127 migration** and **[12711 migration statistics](https://www-genesis.destatis.de/genesis/online?operation=statistic&levelindex=0&levelid=1684962399278&code=12711#abreadcrumb)**:

1. For external migration: [12711-0008 Migration between Germany and foreign countries: Germany, years, nationality, countries of origin / destination](https://www-genesis.destatis.de/genesis//online?operation=table&code=12711-0008&bypass=true&levelindex=1&levelid=1685788618051#abreadcrumb) 
2. For internal migration: [12711-0022 Migration between the Länder: Land of origin, Land of destination, years, nationality, sex](https://www-genesis.destatis.de/genesis//online?operation=table&code=12711-0022&bypass=true&levelindex=1&levelid=1685788618051#abreadcrumb)
3. For data about sex and age: [12711-0006 Migration between Germany and foreign countries: Germany, years, nationality, sex, age years](https://www-genesis.destatis.de/genesis//online?operation=table&code=12711-0006&bypass=true&levelindex=1&levelid=1685788618051#abreadcrumb)

The data sets were preprocessed to suit the workflow. No changes to the data were made niether data were dropped. Only the name of the columns were adjusted.

# Installation instructions

This project is written using python 3 and it is important to have the following packages installed in order to succesfully run it: ***pandas*** and ***seaborn***.


1. Pandas 

	If you have anaconda, install with:
	
		$ conda install pandas
	
	Otherwise refer to the [installation guide](https://pandas.pydata.org/docs/getting_started/install.html) of the [pandas documentation](https://pandas.pydata.org/docs/index.html)
	
2. Seaborn

		$ pip install seaborn

# Usage guide

## Migration summary

This project is composed from 3 main programs wich might be used independently or altogether for a quick summary. If used in the summary mode, simply run `migration_summary.py`. You can run it without arguments and it'll plot a summary containing information about:

- migration in the past 6 years from 2021 
- 5 origin countries in the world with the most migrants coming to Germany
- 5 federal countries receiving most migration
- Sex from migrants with 10, 20, 30, 40 and 50 years

It takes corresponding datasets and save output plots with default file names in the results folder.

	$ python bin/migration_summary.py
	
However the name of the output files can be changed with positional arguments. There are four outputfiles but if only some names are given, it'll order the names as follows: (external migration line, external 

	$ python bin/migration_summary.py results/first_name.png ...

If specific information wants to be plotted, such as specific age span, sex, number of year, number of countries or specific country, it can be done with the following flags:

- `-y, --years` number of years to be plotted (max 21)
- `-nc, --numcountries` number of countries to be plotted (ordered by the n countries with most migrants)
- `-c, --country` country to be plotted
- `-fc, --federalcountry` federal country to be plotted
- `-age, --age_span ` list containing age span to be plotted
- `-s, --sex` sex to be plotted

e.g. the following program plots the 8 past years from 7 most migrant countries world (and federal) and female kids with 5, 6, 7, 8, 9 and 10 years

	$ python bin/migration_summary.py -y 8 -nc 7 -age 5 6 7 8 9 10 -s female
	
If I want to see Colombia and general information in the past 3 years:

	$ python bin/migration_summary,py -y 3 -c Colombia
	

> **Note:** The flags will only change information for some of the plots but not for all of them, as not every data set has complete information. External migration does not contain information about sex and age and sex and age does not consider country.

The summary program is built upon three other programs which plot specific information about external migration, internal migration and sex and age. These programs can also be used from the bash so that the arguments are only applied to specific plots. It'll allow to have more control over the plots.

## External migration

This program plots a line and a bar plot with countries and years and runs under:

	$ python bin/external_migration.py
	
The names of plots can be changed positionally (but are given by default):

	$ python bin/external_migration.py results/first_name.png ... 
	
optional arguments:

- `-y, --years` number of years to be plotted (max 21)
- `-nc, --numcountries` number of countries to be plotted (ordered by the n countries with most migrants)
- `-c, --country` country to be plotted
- `-k, --federalcountry` federal country to be plotted

It plots a bar and a line plot with information about countries from migrants. Specifically in this program it is possible to only plot one of the possible plots if argument kind is given:

if only bar plot:

	$ python bin/external_migration.py -k bar
	
or specifying name

	$ python bin/external_migration.py results/only_bar.png -k bar
	
if only line:

	$ python bin/external_migration.py results/only_line.png -k bar
	
All other arguments are used as in summary.

## Internal migration

This program plots scatter plot with federal countries, years and sex and runs under:

	$ python bin/internal_migration.py
	
The names of the plot can be changed positionally (but is given by default):

	$ python bin/internal_migration.py results/new_name.png
	
optional arguments:

- `-y, --years` number of years to be plotted (max 21)
- `-nc, --numcountries` number of countries to be plotted (ordered by the n countries with most migrants)
- `-fc, --federalcountry` country to be plotted
- `-s, --sex` sex to be plotted

Importantly in internal migration, if only one federal country is to be plotted. It can be done with the flag `-fc`. The following program plots the males going to Brandenburg in the past 5 years (default).

	$python bin/internal_migration.py -fc Brandenburg -s male
	
All other arguments are used as in summary.

## Sex and age

This program plots a bar plot dicriminating sex and age and runs under:

	$ python bin/sex_age.py
	
The names of plots can be changed positionally (but is given by default):

	$ python bin/sex_age.py results/new_name.png

optional arguments:

- `-y, --years` number of years to be plotted (max 21)
- `-age, --age_span` list containing age span to be plotted
- `-s, --sex` sex to be plotted

Importantly in sex and age is the possibility of giving an age span to be plotted. Which can be used to observe migration of different age groups. By default is 10,20,30,40 and 50 but the following program plots migrants between 70 and 80 years.

	$python bin/sex_age.py -age 70 71 72 73 74 75 76 77 78 79 80
	
All other arguments are used as in summary.

# License

> GPL-3.0-or-later

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
   
Full license text can be recovered [here](COPYING.txt)

# Citation
	cff-version: 1.0.
	title: Important factors of migration to Germany
	message: >-
	  If you use this software, please cite it using the
	  metadata from this file.
	type: software
	authors:
	  - given-names: Alejandra
	    family-names: Camelo Cruz
	    email: camelocruz@uni-potsdam.de
	    affiliation: University of Potsdam, Institute for Informatics and Computational Science
	repository-code: 'https://gitup.uni-potsdam.de/camelocruz/immigration_rse'
	abstract: >
	  This software aims at summarizing important factors of
	  immigration  in Germany, such as: number of immigrants,
	  origin countries, sex, age, and concentration and movement
	  between Bundesländer.
	license: GPL-3.0-or-later
	version: 1.0.
	date-released: '2023-06-04'
	
The information for citation can be used from the [cff file](CITATION.cff) in the root folder

# Contact information

>Alejandra Camelo Cruz
>
>Institute for Informatics and Computational Science, University of Potsdam
>
>camelocruz@uni-potsdam.de