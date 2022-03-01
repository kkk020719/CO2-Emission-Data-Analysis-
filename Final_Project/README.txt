This is a project for COMP202 and in this project, it serves the function to analyze data files containing recorded CO2 emissions per country in the past 267 years

About the data

The data shared with you in the large text file is real data, collected and share by the researchers at Our World in Data.

The files containing data regarding the co2 emissions per countries will have the following information:
• A capitalized string representing the iso code of a given country. The ISO country codes are internationally recognized codes that designate every country.
• The name of the country
• A four digit integer representing the year to which the data record belongs.
• A decimal number representing the co2 emissions in millions of tonnes for the specified country in the specified year. Note that some of the decimal numbers are recorded using a comma instead of a dot, which is what is used in French (and in Italian! ;) ) for decimal numbers.
• An integer representing the population of the specified country in the specified year.
Here is how the first three lines of a file containing this data could look like:
QAT,Qatar,2001,41,215,615000
CMR-Cameroon-2001-3.324-16358000
COD Democratic Republic of Congo 2006 1,553 56578000

There will be several modules for this project which includes data_clean_up.py, add_continents.py, build_countries.py, and plot_data.py and I included a description and some examples for each function in these modules. And the image files are some of the graphs plotted after organizing and cleaning up the data given in order to perform some empirical analysis.
