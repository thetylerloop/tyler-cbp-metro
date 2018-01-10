#!/usr/bin/env python

from collections import OrderedDict
import csv
from glob import glob
import re

MSAS = {
    '46340': 'Tyler',
    '47380': 'Waco',
    '48660': 'Wichita Falls',
    '10180': 'Abilene',
    '36220': 'Odessa',
    '30980': 'Longview',
    '17780': 'College Station',
    '19100': 'Dallas',
    '33260': 'Midland'
}

NAICS = {
    '7225//': 'All',
    '722511': 'Full service',
    '722513': 'Limited service'
}

output = []

for filename in glob('data/*.txt'):
    year = re.match('data/cbp([0-9]+)msa.txt', filename).group(1)
    print(year)

    with open(filename) as f:
        reader = csv.DictReader(f)
        
        msa_field_name = 'msa' if 'msa' in reader.fieldnames else 'MSA'
        naics_field_name = 'naics' if 'naics' in reader.fieldnames else 'NAICS'
        emp_field_name = 'emp' if 'emp' in reader.fieldnames else 'EMP'
        est_field_name = 'est' if 'est' in reader.fieldnames else 'EST'

        for row in reader:
            if row[msa_field_name] not in MSAS:
                continue

            if row[naics_field_name] not in NAICS:
                continue

            out_row = OrderedDict([
                ('year', year),
                ('msa', row[msa_field_name]),
                ('msa_name', MSAS[row[msa_field_name]]),
                ('naics', row[naics_field_name]),   
                ('naics_name', NAICS[row[naics_field_name]]),
                ('emp', row[emp_field_name]),
                ('est', row[est_field_name])
            ])

            output.append(out_row)

with open('output/output.csv', 'w') as f:
    writer = csv.DictWriter(f, fieldnames=output[0].keys())
    writer.writeheader()

    writer.writerows(output)


    