#!/usr/bin/env python

import subprocess
import json
import os
import sys

os.environ["AWS_ACCESS_KEY_ID"] = "?"
os.environ["AWS_SECRET_ACCESS_KEY"] = "?"

#Activate emr on machine cli
subprocess.call("aws configure set preview.emr true",shell=True)

print("Get instance id...")
idprocess = subprocess.Popen("curl http://169.254.169.254/latest/meta-data/instance-id", stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
idout, iderr = idprocess.communicate()

if iderr:
    print(iderr)
    raise Exception('Could not find instance id')

print("instance id = " + idout)

print("Get EMR cluster id...")
gettag = "aws ec2 describe-instances --instance-ids " + idout
tagprocess = subprocess.Popen(gettag, stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
out, err = tagprocess.communicate()

if err:
    print(err)
    raise Exception('Could not find cluster id')

j = json.loads(out)
tags = j["Reservations"][0]["Instances"][0]["Tags"]
for key, value in enumerate(tags):
        if value['Key'] == 'aws:elasticmapreduce:job-flow-id':
                item = value['Value']

print ("EMR Cluster Id = " + item)

print("Set the cluster visible to all...")
viscommand = "aws emr set-visible-to-all-users --visible-to-all-users --job-flow-ids " + item
print ("Vis command = " + viscommand)
visprocess = subprocess.Popen(viscommand, stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
visout, viserr = visprocess.communicate()

if viserr:
    print(viserr)
    raise Exception('Could not set cluster to visible')


#Build tags command
tagcommand = "aws emr add-tags --resource-id " + item + " --tags"

if len(sys.argv) % 2 != 1:
    raise Exception('Tags argument number is invalid')

i = 1
while i < len(sys.argv):
    tagcommand = tagcommand + " Key=" + sys.argv[i] + ",Value='" + sys.argv[i + 1] + "'"
    i = i + 2

#tagcommand = "aws emr add-tags --tags Key=Eitan,Value=WasHere --resource-id " + item["Value"]

print ("Tag command = " + tagcommand)
tagsprocess = subprocess.Popen(tagcommand, stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
tagout, tagerr = tagsprocess.communicate()

if tagerr:
    print(tagerr)
    raise Exception('Could not set cluster to visible')
