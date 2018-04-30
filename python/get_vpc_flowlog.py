import boto3
from datetime import datetime as dt
import time
from calendar import timegm
import csv
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--logGroup', help='Log Group Name', default='splunk_cloudwatch')
parser.add_argument('--logStreams', help='Log Stream Names', nargs='+', required=True)
parser.add_argument('--startTime', help="Start time in UTC; 'YYYY-MM-DD HH24:MI:SS'", required=True)
parser.add_argument('--endTime', help="Start time in UTC; 'YYYY-MM-DD HH24:MI:SS'", required=True)
parser.add_argument('--awsRegion', help="Default is us-east-1", default='us-east-1')
args = parser.parse_args()

logGroup = args.logGroup
logStream = args.logStreams
awsRegion = args.awsRegion
# Convert to time object
startDT = time.strptime(args.startTime, '%Y-%m-%d %H:%M:%S')
endDT = time.strptime(args.endTime, '%Y-%m-%d %H:%M:%S')

# Convert to Posix time and convert to ms for AWS
startPosix = timegm(startDT)*1000
endPosix = timegm(endDT)*1000

# csv header
csvHeader = ['interface-id','timestamp','srcaddr','srcport','dstaddr','dstport','protocol','bytes','action','log-status']
headerTest = True

# output csv file
outFile = 'vpcflow_' + dt.now().strftime('%Y%m%d_%H%M%S') + '.csv'

# Convert Posix time to something readable
convPosix = lambda x: dt.utcfromtimestamp(int(x)).strftime('%Y-%m-%d %H:%M:%S')

def writeCSV(d):
	global headerTest
	with open(outFile, 'a', newline='') as csvFile:
		csvWrite = csv.writer(csvFile)
		if headerTest:
			csvWrite.writerow(csvHeader)
			headerTest = False
		for j in d:
			csvWrite.writerow(j)
		
for s in logStream:
	client = boto3.client('logs',region_name=awsRegion)
	resp = client.get_log_events(
		logGroupName=logGroup,
		logStreamName=s,
		startTime=startPosix,
		endTime=endPosix
	)

	rawMsg = [i['message'] for i in resp['events']]
	cleanMsg = [(i[2],convPosix(i[10]),i[3],i[5],i[4],i[6],i[7],i[9],i[12],i[13]) for i in [r.split() for r in rawMsg]]
	writeCSV(cleanMsg)

print('... created csv file {0}'.format(outFile))
