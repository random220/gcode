import sys
import csv
def process_csvfile(csvfile):
    all_lines = []
    fields = []
    with open(csvfile, 'rt', newline='', encoding='utf-8') as f:
        #c = csv.DictReader(f)
        c = csv.reader(f)
        for line in c:
            if len(line) != 14:
                continue
            if line[0] == 'Run Date':
                fields = line
            else:
                dictline = {}
                for i in range(14):
                    dictline[fields[i]] = line[i]
                if 'BOUGHT' in dictline['Action'] or 'SOLD' in dictline['Action']:
                    all_lines.append(dictline)
    return fields, all_lines
                    
content = []
for csvfile in sys.argv[1:]:
    fields, lines = process_csvfile(csvfile)
    content.extend(lines)

with open('input.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fields, extrasaction='raise')

    writer.writeheader()
    for line in content:
        writer.writerow(line)
