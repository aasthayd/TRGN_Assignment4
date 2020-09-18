import sys
import fileinput
import csv
import re


gene_data = 'Homo_sapiens.GRCh37.75.gtf'
print('here')

if len(sys.argv) > 3:
    print('>3')
    index_to_replace_gene_id = int(sys.argv[1].split('-f')[-1])
    input_file_path = sys.argv[2]
    results_file_path = sys.argv[3].replace('>','')

else:
    print('3')
    index_to_replace_gene_id = 0
    input_file_path = sys.argv[1]
    results_file_path = sys.argv[2].replace('>','')

ensembl_dict={}
for each_line_of_text in fileinput.FileInput(gene_data):
    if each_line_of_text.startswith('#'):
        continue
    gene = re.findall(r'^.*?\t.*?\t(.*?)\t', each_line_of_text, re.I)
    ensg_ID = re.findall(r'\"(ENSG.*?)\"', each_line_of_text, re.I) 
    hugo_name = re.findall(r'gene_name "(.*?)"', each_line_of_text, re.I) 

    if gene:
        ensembl_dict[ensg_ID[0]] = hugo_name[0] 
hugo_name_list = []

count_found = 0
count_unknown = 0
with open(input_file_path) as csv_file:
    csv_reader = csv.reader(csv_file)
    for row in csv_reader:
        print(row)
        ensg_ID = row[1].split('.')[0]
        print(ensg_ID)
        hugo = ensembl_dict.get(ensg_ID, 'UNKNOWN')
        row[1] = hugo
        hugo_name_list.append(row)

with open(results_file_path, 'w', newline='') as results_file:
    writer = csv.writer(results_file)
    writer.writerows(hugo_name_list)

