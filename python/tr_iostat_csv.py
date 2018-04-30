# Transforms iostat output file to a csv
# Format specific to iostat -h -y -t -x
#

import re
import argparse
import os
import csv

parser = argparse.ArgumentParser()
parser.add_argument('--inFile', help='The iostat output to parse', required=True)
parser.add_argument('--hostServer', help='The hostname or IP to add with csv data', required=True)
args = parser.parse_args()
input_file = args.inFile
host_server = args.hostServer

date_pattern = re.compile('^\d\d/\d\d/\d\d\d\d')
dev_pattern = re.compile('^xvd')
stat_pattern = re.compile('^\s+\d+\.\d+')

# Need file size to use later to check if we have reached EOF
file_size = os.lstat(input_file).st_size

# Open input file 
f = open(input_file, 'r')

# Open csv output file and write header
output_file = ''.join([input_file, '.csv'])
csv_file = open(output_file, 'w')
csv_writer = csv.writer(csv_file)
csv_header = ['host','date_ts','device','rrqm_s','wrqm_s','r_s','w_s','rkB_s','wkB_s','avgrq-sz','avgqu-sz','await','r_await','w_await','svctm','pct_util']
csv_writer.writerow(csv_header)

# Use to build csv row to write; a: date/timestamp, b: device name, c: iostat list
def build_csv_row(a, b, c):
   csv_row = []
   csv_row.append(host_server)
   csv_row.append(a)
   csv_row.append(b)
   csv_row.extend(c)
   return csv_row

line = f.readline()

try:
   while line:
      is_m_date = date_pattern.match(line)
      ### If line is a date; then start processing stat block
      if is_m_date is not None:
         date_ts = (is_m_date.string).strip('\n')
   
         #### Process iostat lines until another date is encountered; set process_stat_block to False if eventually encounter a date
         process_stat_block = True
         while process_stat_block:
            line = f.readline()
            # Check if reached EOF
            if f.tell() == file_size:
               raise EOFError
            is_m_date = date_pattern.match(line)
            #### If line not a date; then process
            if is_m_date is None:
               # If line is a device; save the device name
               is_m_dev = dev_pattern.search(line)
               if is_m_dev is not None:
                  dev_name = line.strip('\n')
                  ##### Read the next line which should be stats for the device
                  line = f.readline()
                  if f.tell() == file_size:
                     raise EOFError
                  is_m_stat = stat_pattern.search(line)
                  if is_m_stat is not None:
                     stat_line = line.strip('\n')
                     stat_list = stat_line.split()
                     # write csv output
                     csv_writer.writerow(build_csv_row(date_ts, dev_name, stat_list))
            #### Date encountered, exit process_stat_block
            else:
               process_stat_block = False
   
      ### If line is not a date; then read another line
      else:
         line = f.readline()
except EOFError as e:
   f.close()
   csv_file.close()


print('... created {0} csv file'.format(output_file))
