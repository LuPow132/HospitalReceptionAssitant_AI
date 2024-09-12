# importing csv module
import csv

# csv file name
filename = "CSV_Test/sample_data.csv"

# initializing the titles and rows list
fields = []
rows = []

# reading csv file
with open(filename, 'r', encoding="utf8") as csvfile:
    # creating a csv reader object
    csvreader = csv.reader(csvfile)

    # extracting field names through first row
    fields = next(csvreader)

    # extracting each data row one by one
    for row in csvreader:
        rows.append(row)
  # get total number of rows
    print(f"Total no. of rows: {csvreader.line_num}" )

# printing the field names
print('Field names are:' + ', '.join(field for field in fields))

# printing first 5 rows
# print('\nFirst 5 rows are:\n')
# for row in rows[:5]:
#     # parsing each column of a row
#     for col in row:
#         print("%10s" % col, end=" "),
#     print('\n')

data = ['2','Tustong Tongnumpen','17','178','male','60','ปวดหัว ตัวร้อน']
with open(filename, 'a', encoding="utf8") as csvfile:
    # creating a csv writer object
    csvwriter = csv.writer(csvfile)
    # writing the data rows
    csvwriter.writerows(rows)