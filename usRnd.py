import csv
import subprocess

class SortedDisplayDict(dict):
   def __str__(self):
       return "{" + ", ".join("%r: %r" % (key, self[key]) for key in sorted(self)) + "}"

with open('coord.csv') as f:
    clusterName = dict(filter(None, csv.reader(f)))
clusterName = SortedDisplayDict(clusterName)
print clusterName
dictionary_1 = {}
dictionary_2 = {}

for key in sorted(clusterName):
	machineName = clusterName[key]
	cluster_value_1 = subprocess.Popen('sshpass -p "qauv13" ssh -o StrictHostKeyChecking=no -t QAUV@10.31.15.242 curl {0}| grep -Po "\d+.\d*.\d*-\d*"'.format(machineName), stdout=subprocess.PIPE, stderr=None, shell=True)
	cluster_value_2 = subprocess.Popen('sshpass -p "qauv13" ssh -o StrictHostKeyChecking=no -t QAUV@10.31.15.242 curl {0}| grep -c true'.format(machineName), stdout=subprocess.PIPE, stderr=None, shell=True)
	output_1 = cluster_value_1.communicate()
	output_2 = cluster_value_2.communicate()	
	dictionary_1[key] = output_1[0]
        dictionary_2[key] = output_2[0]

f = open('/var/www/html/COORDVersion.html','w')

message = """<!DOCTYPE html>
<html>
<head>
</head>
<body>
<table border=5 style="width:50%" CELLPADDING="4" CELLSPACING="14">
  <tr style="background-color:Aqua; align=left;">
        <th>ENV</th>
        <th>STATUS</th>
        <th>Current Version</th>
  </tr>
"""

for key in sorted(dictionary_1):
	print "################"
	print  dictionary_2[key]
        if ("4" in dictionary_2[key]):
                message+= "<tr style='background-color:White'><td>{1}</td><td>................<img src='./green.gif' alt='down'>................</td><td>{2}</td></tr>".format( clusterName[key],key, dictionary_1[key],dictionary_2[key])
        else:
		message+= "<tr style='background-color:White' width=20%><td>{1}</td><td>................<img src='./red.gif' alt='down'>................</td><td>{2}</td></tr>".format( clusterName[key],key, dictionary_1[key],dictionary_2[key])

print message

f.write(message)
f.close()



