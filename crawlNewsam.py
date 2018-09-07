from os import system
output_file_name = 'results.csv'
system('scrapy crawl newsam -o ' + output_file_name + ' -t csv')