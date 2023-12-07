import csv

walmart_url_notsure = []
walmart_url_incorrect = []
walmart_url_exact = []
with open('input_files/urls.csv', 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        if row['Match_Type'] == 'Not Sure':
            walmart_url_notsure.append(row['Comp_Url'])
        if row['Match_Type'] == 'Incorrect Match':
            walmart_url_incorrect.append(row['Comp_Url'])
        if row['Match_Type'] == 'Exact Match':
            walmart_url_exact.append(row['Comp_Url'])


# print only the first 15 elements
print(walmart_url_notsure[:15])
print(walmart_url_incorrect[:15])
print(walmart_url_exact[:15])