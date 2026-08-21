## random script that creates a CSV of 50 fake projects at projects.csv

import os
import csv
import random

project_name = ['Atlas','Horizon','Nimbus']
client = ['Acme Corp','Globex','Initech']
status = ['Active','Hold','Completed']

with open("data/projects.csv","w",newline="") as f:
 writer = csv.writer(f)
 writer.writerow(['project_id','project_name','client','status'])
 for i in range(1,51):
    project_1 = random.choice(project_name)
    client_1 = random.choice(client)
    status_1 = random.choice(status)
    writer.writerow([i,project_1,client_1,status_1])

