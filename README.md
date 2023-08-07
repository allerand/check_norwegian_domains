# check_norwegian_domains

Takes a template with several possible websites using norwegian language and checks if they're available or not.


The scraper automatically creates and saves the data in the domain_status.csv file. 

A different column is created every day (7/8/2023 would be today's as an example) and it can be interrupted within the same day and run the script again without losing what has been done. When it resumes it will resume from the last scraped row. 

Also, auto save every 1000 scraped rows. The next day it will start from 0 in a new column with tomorrow's date.
