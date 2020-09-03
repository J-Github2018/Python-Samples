#!/usr/bin/env python3

import requests
import json
import csv
import os
import sys


#Variables
user = []
group = []
permissions = []
repoKey = []
URLS = ["https://artifactory.com","http://artifactorydummyURL2","http://DummyURL3"]

#This function creates folders in the current working directory
def create_folder():
    try:
        os.mkdir('user')
        print("Directory user Created ")
    except FileExistsError:
        print('Directory user already exists')

    try:
        os.mkdir('group')
        print("Directory group Created ")
    except FileExistsError:
        print('Directory group already exists')

    try:
        os.mkdir('permissions')
        print("Directory permissions Created ")
    except FileExistsError:
        print('Directory permissions already exists')

    try:
        os.mkdir('repoKey')
        print("Directory repoKey Created ")
    except FileExistsError:
        print('Directory repoKey already exists')


#This function ask for the file location of the csv file and then appends the rows to the Variables,
#please note that this function is designed to retrieve data from 4 columns.
def get_data():
    file_path = './repolist.csv'
    with open(file_path) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        next(readCSV) # Skip the first 'title' row.
        for row in readCSV:
            columnA = user.append(row[0])
            columnB = group.append(row[1])
            columnC = permissions.append(row[2])
            columnD = repoKey.append(row[3])

            if row[0] != '': #this if conditional gets rid of '' from the list
                columnA
            if row[1] != '': #this if conditional gets rid of '' from the list
                columnB
            if row[2] != '': #this if conditional gets rid of '' from the list
                columnC
            if row[3] != '': #this if conditional gets rid of '' from the list
                columnD

#This function run the get requests api call and if the api call passes the status code of 200 it then creates the json files and puts the json file in the appropiate folders.
def get_replication_request():
  tmplist = []
  if len(user[0]) > 2:
      for get in user:
          user_data = requests.get('https://localhost/artifactory/api/security/users/{}'.format(get), auth=('admin','*********************'))
          if user_data.status_code == 200:
              tmplist.append(user_data.json())
          else:
            print('User column Error!!! You received response', user_data)
      with open('user/user.json', 'a') as f:
        json.dump(tmplist, f)
        print('user.json has been created, please check under the user directory')

  if len(group[0]) > 2:
      tmplist2 = []
      for get in group:
          group_data = requests.get('https://localhost/artifactory/api/security/groups/{}'.format(get), auth=('admin','*********************'))
          if group_data.status_code == 200:
              tmplist2.append(group_data.json())
          else:
            print('Group column Error!!! You received response', group_data)
      with open('group/group.json', 'a') as f:
          json.dump(tmplist2, f)
          print('group.json has been created, please check under the group directory')

  if len(permissions[0]) > 2:
      tmplist3 = []

      for get in permissions:
          permissions_data = requests.get('https://localhost/artifactory/api/security/permissions/{}'.format(get), auth=('admin','*********************'))
          if permissions_data.status_code == 200:
              tmplist3.append(permissions_data.json())
          else:
            print('Permissions column Error!!! You received response', permissions_data)
      with open('permissions/permissions.json', 'a') as f:
          json.dump(tmplist3, f)
          print('permissions.json has been created, please check under the permissions directory')

  if len(repoKey[0]) > 2:
      tmplist4 = []

      for get in repoKey:
          repoKey_data = requests.get('https://localhost/artifactory/api/repositories/{}'.format(get), auth=('admin','*********************'))
          if repoKey_data.status_code == 200:
              tmplist4.append(repoKey_data.json())
          else:
            print('Repokey column Error!!! You received response', repoKey_data)
      with open('repoKey/repoKey.json', 'a') as f:
          json.dump(tmplist4, f)
          print('repoKey.json has been created, please check under the repoKey directory')

#What this function does is runs a put request using the payload information provided and using a looping through the repoKey list.
def update_replication():
    count = 1
    for repo in repoKey:
        payload = {
                "cronExp":"0 0/9 14 * * ?",
                "enableEventReplication":"true",
                "replications":[
                                    {
                                        "url": "https://localhost/artifactory/{}".format(repo),
                                        "socketTimeoutMillis": 15000,
                                        "username": "dummyUser",
                                        "password": "DummyPassword",
                                        "syncStatistics": "false",
                                        "enabled": "true",
                                        "syncDeletes": "false",
                                        "syncProperties": "true",
                                        "repoKey": "{}".format(repo),
                                        "enableEventReplication": "false"
                                    }
                                ]
                   }
        headers = {"Content-Type": "application/json"}
        try:
            r_put = requests.put(url='http://localhost2:6090/artifactory/api/replications/multiple/{}'.format(repo),json=payload, auth=('admin', '*********************'), headers=headers)
        except requests.exceptions.RequestException as e:
            print('ERROR: The repo: ' + repo + ' Falied due to the following error =====>', e)
            sys.exit(1)
        print('For Repo ' + repo + ' The status of this api call was (' + str(r_put) + ')and this is API request # ' + str(count).format(repo))
        count+= 1
    print('Api Put request complete, the following')

#What this function does is runs a post request using the payload information provided and using a looping through the repoKey list.
def trigger_replication():
    count = 1
    for repo in repoKey:
        payload = {
            "repoKey":"{}".format(repo)
        }
        headers = {"Content-Type": "application/json"}
        try:
            r_post = requests.post(url='http://rtp-wapl-arti1.cisco.com:6090/artifactory/ui/admin/repositories/executeall?repreal_tesoKey={}'.format(repo),json=payload, auth=('admin', '*********************'), headers=headers)
        except requests.exceptions.RequestException as e:
            print('ERROR: The repo: ' + repo + ' Falied due to the following error =====>', e)
            sys.exit(1)
        print('For Repo {}, The status of this api call was (' + str(r_post) + ')and this is API request # ' + str(count).format(repo))
        count+= 1
    print('Api Post request complete')


def get_replication_configs():
    count = 1
    for repo in repoKey:
        try:
            r = requests.get(url='https://localhost/artifactory/api/replications/{repo}'.format(repo=repo), auth=('admin', '*********************'))
            print("I sent a request hitting the following URL", r.url)
            print(json.dumps(r.json(), indent=2))
            print('\n')
        except requests.exceptions.RequestException as e:

            print('ERROR: The repo: ' + repo + ' Failed due to the following error =====>', e)
            sys.exit(1)
        count+= 1
    print('>>>>>>>>> Api Get request complete')
    print('\n')


def delete_replication_configs():
    print('###### Backup Config #####')
    print('Saving Config-Bkup.xml in current working directory for backup purposes, before deletion')
    url = requests.get(url='https://localhost/artifactory/api/system/configuration',auth=('admin', '*********************'))
    if url.status_code == 200:
        with open('./Config-Bkup.xml', 'wb') as f:
            f.write(url.content)
    else:
        print('ERROR: I could not backup the config.xml prior to deleting replication config data. Aborting')
        sys.exit(1)
    print('###### Backup Config Complete #####')
    print('\n')
    print('>>>>>>>>> Api Delete request Starting')

    count = 1
    for url in URLS:
       for repo in repoKey:
           try:
               r = requests.delete(url='https://localhost/artifactory/api/replications/{repo}?url={url}/artifactory/{repo}'.format(repo=repo, url=url), auth=('admin', '*********************'))
               print("I sent a delete request hitting the following URL", r.url)

           except requests.exceptions.RequestException as e:

               print('ERROR: The repo: ' + repo + ' Failed due to the following error =====>', e)
               sys.exit(1)
           print('For Repo ' + repo + ' The status of this api call was (' + str(r) + ') and this is API request # ' + str(count).format(repo))
           print('\n')
           count+= 1
    print('>>>>>>>>> Api Delete request complete')
    print('\n')




def main():
    #create_folder()
    #get_data()
    #get_replication_request()
    #update_replication()
    #trigger_replication()
    #get_replication_configs()
    #delete_replication_configs()

main()