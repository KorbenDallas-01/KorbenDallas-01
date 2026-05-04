import os
import re

# Folder containing the PDF files
folder_path = os.path.join(os.path.expanduser("~"), "Desktop", "certs", "pdfs")
out_file = os.path.join(os.path.expanduser("~"), "Desktop", "certs", "outlist.csv")
csv_file = os.path.join(os.path.expanduser("~"), "Desktop", "certs", "list.csv")
# print(folder_path)
# print(out_file)

# Function to extract numbers from filenames for correct sorting
# def extract_number(filename):
#     matches = re.findall(r'\d+', filename)
#     return int(matches[-1]) if matches else float('inf')
#
# files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]

# Sort the files by the number in the filename
# sorted_files = sorted(files, key=extract_number)

# Print sorted filenames
# for file in sorted_files:
#     print(file)


# Export sorted filenames to a file
# with open(out_file, 'w') as output_file:
#     for file in sorted_files:
#         output_file.write(file + '\n')

# print("Sorted filenames have been written to sorted_filenames.txt")

sorted_files = sorted(
    [f for f in os.listdir(folder_path) if f.endswith('.pdf')],
    key=lambda f: int(re.findall(r'\d+', f)[-1]) if re.findall(r'\d+', f) else float('inf')
)
print(len(sorted_files))
print(sorted_files)


# for fi in sorted_files:
#     print(fi)
# with open(out_file, 'w') as output_file:
#     for file in sorted_files:
#         output_file.write(file + '\n')
# import names
import csv
names = []
with open(r'C:\Users\IBE\Desktop\certs\NamesList.csv', 'r', encoding='utf-8') as rf:
    reader = csv.reader(rf, delimiter=',')
    next(reader, None)
    for row in reader:
      # print(row[1])
      # print("".join(str(row[1]))
      names.append(row[1])

print(names)
print(len(names))

with open(out_file, 'w', encoding='utf-8', newline='') as cs:
    writer = csv.writer(cs)
    writer.writerow(['Name', 'File'])
    for name, file in zip(names, sorted_files):
        writer.writerow([name, file])









