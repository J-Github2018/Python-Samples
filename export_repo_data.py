#!/usr/bin/env python3

import sys
import requests
import csv
import time



repoKey = []



def get_csv():
    #file_path = input('Please enter csv file location to parse: ')
    file_path = './repolist.csv'
    with open(file_path, encoding='utf-8-sig') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        #next(readCSV) # Skip the first 'title' row.
        for row in readCSV:
            columnA =  repoKey.append(row[0])

            if row[0] != '': #this if conditional gets rid of '' from the list
               columnA


def trigger_export():
    count = 1
    for repo in repoKey:
         payload = {
                      "action":"repository",
                      "repository": "{}".format(repo),
                      "path": "/auto/solar_artifactory1",
                      "excludeMetadata": True,
                      "m2": False,
                      "verbose": True,
                  }
         headers = {"Content-Type": "application/json"}
         if len(repo) > 0:

             try:
                 r_post = requests.post(
                     url='http://localhost:6090/artifactory/ui/artifactexport/repository', json=payload, auth=('admin', '****************'), headers=headers)
                 r_post.close()
             except requests.exceptions.RequestException as e:
                 print('ERROR: The repo: ' + repo + ' Falied due to the following error =====>', e)
                 sys.exit(1)

             print('For {}, The status of this api call was ('.format(repo) + str(r_post) + ')and this is API request # ' + str(count))

             count += 1
             time.sleep(1)
    print('Api Post request complete')




def main():
    get_csv()
    trigger_export()


main()

