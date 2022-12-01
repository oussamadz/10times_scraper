# 10times_scraper
## Introduction
This Scrapy powered script is for scraping venues out of 10times.com website, it consists of scraping venues data + images available for each venue.
For security reasons, delai between downloads is set to 3s any less will cause ip block, the only better way is to use paid proxy rotation service for the 
free proxy will cause more unnecessary delai. 
## Requirements
### scrapy
### pillow
### pandas
## Usage
simply type in :
`scrapy crawl venues -o data.csv`
this way the data will be saved in "data.csv" file and images in "images" dir.
