#!/usr/bin/env python3

import requests
import pandas
import stdiomask


def storageinfo():
    global URL
    env = input("Please select the env you want to query? [QA, Stage, or Prod]: ").upper()
    if env in ['QA', 'STAGE', 'PROD']:

        user = input("Please enter a " + f'{env}' + " username: ")
        password = stdiomask.getpass(prompt="Please enter " + f'{env}' + ' password for user ' + f'{user}: ')

        if env == 'PROD':
            site = input('Please enter a site location to query [SJC, RTP-SAT, RTP-DR, GPK, BGL, NTN]: ').lower()
            if site == 'rtp-dr':
                site = 'rtp'
                URL = f'http://{site}-wapl-localhost.com:6090'
            elif site == 'sjc':
                URL = f'http://{site}-wapl-localhost.com:6090'
            elif site == 'rtp-sat':
                site = 'rtp'
                URL = f'http://{site}-wapl-localhosts4.com:6090'
            elif site == 'ntn':
                URL = f'http://{site}-wapl-localhost2.com:6090'
            elif site == 'gpk' or site == 'bgl':
                URL = f'http://{site}-wapl-localhost3.com:6090'
            else:
                print('Please re-run script and select one of the following PROD sites [SJC, RTP-SAT, RTP-DR, GPK, BGL, NTN]')

        elif env == 'STAGE':
            site = input('Please enter a site location to query [SJC, RTP-DR, GPK]: ').lower()
            if site == 'rtp-dr':
                site = 'rtp'
                URL = f'http://{site}-stg-localhost1.com:6090'
            elif site == 'sjc' or site == 'gpk':
                URL = f'http://{site}-stg-localhost1.com:6090'
            else:
                print('Please re-run script and select one of the following STAGE sites [SJC, RTP-DR, GPK,]')

        elif env == 'QA':
            site = input('Please enter a site location to query [SJC, RTP-DR,GPK]: ').lower()
            if site == 'rtp-dr':
                site = 'rtp'
                URL = f'http://{site}-qa-localhost1.com:6090'
            elif site == 'sjc' or site == 'gpk':
                URL = f'http://{site}-qa-localhost1.com:6090'
            else:
                print('Please re-run script and select one of the following QA sites [SJC, RTP-DR, GPK,]')
        else:
            print('Please re-run script and select one of the following env [QA, Stage, or Prod]')
        try:

            print(f'Querying API endpoint, please wait while I fetch the data.........')
            session = requests.Session()

            r = session.get(url=f'{URL}/localhost/api/storageinfo', auth=(user, password), timeout=None)

            if r.status_code != 200:
                print('Script failed due to the following status code  ===>', r.status_code)
                exit(1)

            dataJson = r.json()
            data = dataJson['storageSummary']['repositoriesSummaryList']
            df = pandas.DataFrame(data=data)

            print(
                'Done, Saving the file ' + f'localhost_{env}_{site.upper()}_Storage_Quota_report.csv' + ' to current working directory')
            df.to_csv(f'./localhost_{env}_{site.upper()}_Storage_Quota_report.csv', index=False)

        # catch all the exceptions
        except requests.exceptions.RequestException as e:
            print('ERROR: Request failed due to the following error =====>', e)

    else:
        print('Please only enter, [QA, Stage, or Prod]')


storageinfo()