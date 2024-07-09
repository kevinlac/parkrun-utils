# Parkrun-Utils
Tool to analyze parkrun data.
Currently only lists locations listed at https://www.parkrun.com.au/special-events/

## Features
See graphs and summary statistics for the recorded times of a given parkrun  
Filter data by categories (All, Only Male, Only Female)

## Data Collection
Data is scraped from the parkrun website using BeautifulSoup  
Note that only times with complete data are considered (No "Unknown" rows, no rows with missing Gender/Agegroup)
