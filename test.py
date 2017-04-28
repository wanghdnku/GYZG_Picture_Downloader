import csv
csvfile = open('/Users/hayden/Desktop/hello.csv', 'w')
writer = csv.writer(csvfile)
writer.writerow(['title', 'summary', 'year', 'id', 'count', 'link'])
csvfile.close()