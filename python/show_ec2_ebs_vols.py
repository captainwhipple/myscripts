# show_ec2_ebs_vols.py
#
# Prints the EBS volume IDs associated with an EC2 instance's mount points.
# Note that EBS volume /dev device IDs on the EC2 instance may look a bit different from what SDK or console display. 
# (i.e. /dev/xvda rather than /dev/sda)
# Typically the last letter of the devices should be the same (i.e. /dev/xvda /dev/sda both end with 'a' which helps identify the volume)
#
# Run like so...
# python3 show_ec2_ebs_vols.py --instanceID i-073e4bbf797ee5b0e
 
import argparse
import boto3

parser = argparse.ArgumentParser()
parser.add_argument("--instanceID", help="AWS EC2 Instance ID", required=True)
parser.add_argument("--awsRegion", help="AWS Region", default="us-east-1")
args = parser.parse_args()

ec2Resource = boto3.resource('ec2', region_name=args.awsRegion)
ec2Instance = ec2Resource.Instance(args.instanceID)

for i in ec2Instance.volumes.all():
   a = i.attachments[0]
   print("{1}: {0}".format(a['VolumeId'], a['Device']))

