#Final version of the code to create PR for disk expansion automatically

#HOW TO RUN THIS CODE:
# Step 1: set following env variables on your local pc, using the code shown below:
  # import os
  # Set the environment variable
  # os.environ['BITBUCKET_USERNAME'] = 'abhi.lalwani'
  # os.environ['BITBUCKET_PASSWORD'] = 'your password here'
  # Verify that the environment variable is set
  # print(os.getenv('BITBUCKET_USERNAME')) 
  # print(os.getenv('BITBUCKET_PASSWORD'))
# step 2 :
  # Following are the input variables explained, needed for this code:
  # 1. OLD_DISK_SIZE='2000' This is the old size of the disk in string that needs to be entered as an input variable 
  # 2. NEW_DISK_SIZE='4000' This is the new size of the disk in string that needs to be entered as an input variable 
  # 3. BRANCH_NAME = this is branch name in string that needs to be entered as an input variable, which will be created by this code, so make sure its not existing, otherwise the code will error out.
  # 4. TARGET_FOLDER = 'the folder from where this python is being executed' + 'you need to add the path to the main.tf' 
  # for example I am running this python from 'C:/Users/abhi.lalwani/testPRauto/' and here the root-mssql repo will be cloned by this code automatically,
  # so we need to add the path to the main.tf in root-mssql repo where the change is being made, 
  # for example: 'C:/Users/abhi.lalwani/testPRauto/root-mssql/prod/regions/us-central1/environments/p/compute/sql/f/fcsag03'
  
# Example to run this code:  
  # create_pr_disk_expansion(OLD_DISK_SIZE='2000',NEW_DISK_SIZE='4000',BRANCH_NAME='ds-12356-test-auto-pr',TARGET_FOLDER='C:/Users/abhi.lalwani/testPRauto4/root-mssql/prod/regions/us-central1/environments/p/compute/sql/f/fcsag03')

import os
import subprocess
import requests
from base64 import b64encode

def create_pr_disk_expansion(OLD_DISK_SIZE,NEW_DISK_SIZE,BRANCH_NAME,TARGET_FOLDER):
    
    # Configuration
    BITBUCKET_SERVER_URL = 'https://stash.blackline.corp'
    REPO_PROJECT = 'TFM'
    REPO_SLUG = 'root-mssql'
    PR_TITLE = 'disk expansion Update'
    PR_DESCRIPTION = 'This PR contains automated updates to the infrastructure.'
    FILE_NAME = 'main.tf'
    OLD_VARIABLE_LINE = f'data_disk_size     = {OLD_DISK_SIZE}'
    NEW_VARIABLE_LINE = f'data_disk_size     = {NEW_DISK_SIZE}'
    print(NEW_VARIABLE_LINE)
    
    # Authentication (using personal access token or username and password)
    USERNAME = os.getenv('BITBUCKET_USERNAME')
    PASSWORD = os.getenv('BITBUCKET_PASSWORD')
    AUTH = b64encode(f'{USERNAME}:{PASSWORD}'.encode()).decode()
    
    HEADERS = {
        'Authorization': f'Basic {AUTH}',
        'Content-Type': 'application/json'
    }
    
    def run_command(command):
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout = result.stdout.decode('utf-8').strip()
        stderr = result.stderr.decode('utf-8').strip()
        if stdout:
            print("stdout:", stdout)
        if stderr:
            print("stderr:", stderr)
        return stdout
        return result.stdout.decode('utf-8').strip()
    
    def create_branch():
        run_command(f'git checkout -b {BRANCH_NAME}')
    
    def update_variable():
        file_path = os.path.join(TARGET_FOLDER, FILE_NAME)
        print('update variable: '+file_path)
        with open(file_path, 'r') as file:
            content = file.read()
        
        updated_content = content.replace(OLD_VARIABLE_LINE, NEW_VARIABLE_LINE)
        print(updated_content)
        
        with open(file_path, 'w') as file:
            file.write(updated_content)
        
        run_command('git add .')
        run_command(f'git commit -m "updated disk"')
    
    def push_branch():
        run_command(f'git push --set-upstream origin {BRANCH_NAME}')
    
    def create_pull_request():
        url = f'{BITBUCKET_SERVER_URL}/rest/api/1.0/projects/{REPO_PROJECT}/repos/{REPO_SLUG}/pull-requests'
        data = {
            "title": PR_TITLE,
            "description": PR_DESCRIPTION,
            "state": "OPEN",
            "open": True,
            "closed": False,
            "fromRef": {
                "id": f"refs/heads/{BRANCH_NAME}",
                "repository": {
                    "slug": REPO_SLUG,
                    "name": None,
                    "project": {
                        "key": REPO_PROJECT
                    }
                }
            },
            "toRef": {
                "id": "refs/heads/master",
                "repository": {
                    "slug": REPO_SLUG,
                    "name": None,
                    "project": {
                        "key": REPO_PROJECT
                    }
                }
            },
            "locked": False,
            "reviewers": [
            {
              "user": {
                "name": "dhamo.murugesan",
                "emailAddress": "dhamo.murugesan@blackline.com",
                "id": 6256,
                "displayName": "Dhamo Murugesan",
                "slug": "dhamo.murugesan",
                "type": "NORMAL",
                "links": {
                  "self": [
                    {
                      "href": "https://stash.blackline.corp/users/dhamo.murugesan"
                    }
                  ]
                }
              },
              "role": "REVIEWER",
              "status": "UNAPPROVED"
            }, 
            {
              "user": {
                "name": "rajeev.chaudhary",
                "emailAddress": "rajeev.chaudhary@blackline.com",
                "id": 6115,
                "displayName": "Rajeev Chaudhary",
                "slug": "rajeev.chaudhary",
                "type": "NORMAL",
                "links": {
                  "self": [
                    {
                      "href": "https://stash.blackline.corp/users/rajeev.chaudhary"
                    }
                  ]
                }
              },
              "role": "REVIEWER",
              "status": "UNAPPROVED"
            },
            {
              "user": {
                "name": "neha.mahendra",
                "emailAddress": "neha.mahendra@blackline.com",
                "id": 6873,
                "displayName": "Neha Mahendra",
                "slug": "neha.mahendra",
                "type": "NORMAL",
                "links": {
                  "self": [
                    {
                      "href": "https://stash.blackline.corp/users/neha.mahendra"
                    }
                  ]
                }
              },
              "role": "REVIEWER",
              "status": "UNAPPROVED"
            },
            {
              "user": {
                "name": "Jed.Nguyen",
                "emailAddress": "Jed.Nguyen@blackline.com",
                "id": 913,
                "displayName": "Jed Nguyen",
                "slug": "jed.nguyen",
                "type": "NORMAL",
                "links": {
                  "self": [
                    {
                      "href": "https://stash.blackline.corp/users/jed.nguyen"
                    }
                  ]
                }
              },
              "role": "REVIEWER",
              "status": "UNAPPROVED"
            },
            {
              "user": {
                "name": "sauras.pandey",
                "emailAddress": "sauras.pandey@blackline.com",
                "id": 6869,
                "displayName": "Sauras Pandey",
                "slug": "sauras.pandey",
                "type": "NORMAL",
                "links": {
                  "self": [
                    {
                      "href": "https://stash.blackline.corp/users/sauras.pandey"
                    }
                  ]
                }
              },
              "role": "REVIEWER",
              "status": "UNAPPROVED"
            },
            {
              "user": {
                "name": "Anthony.Kautz",
                "emailAddress": "Anthony.Kautz@blackline.com",
                "id": 3007,
                "displayName": "Anthony Kautz",
                "slug": "anthony.kautz",
                "type": "NORMAL",
                "links": {
                  "self": [
                    {
                      "href": "https://stash.blackline.corp/users/anthony.kautz"
                    }
                  ]
                }
              },
              "role": "REVIEWER",
              "status": "UNAPPROVED"
            },
            {
              "user": {
                "name": "sowmya.bhat",
                "emailAddress": "sowmya.bhat@blackline.com",
                "id": 6624,
                "displayName": "Sowmya Bhat",
                "slug": "sowmya.bhat",
                "type": "NORMAL",
                "links": {
                  "self": [
                    {
                      "href": "https://stash.blackline.corp/users/sowmya.bhat"
                    }
                  ]
                }
              },
              "role": "REVIEWER",
              "status": "UNAPPROVED"
            },
            {
              "user": {
                "name": "Amit.Wadhawan",
                "emailAddress": "amit.wadhawan@blackline.com",
                "id": 4513,
                "displayName": "Amit Wadhawan",
                "slug": "amit.wadhawan",
                "type": "NORMAL",
                "links": {
                  "self": [
                    {
                      "href": "https://stash.blackline.corp/users/amit.wadhawan"
                    }
                  ]
                }
              },
              "role": "REVIEWER",
              "status": "UNAPPROVED"
            },
            {
              "user": {
                "name": "craig.gall",
                "emailAddress": "craig.gall@blackline.com",
                "id": 4740,
                "displayName": "Craig Gall",
                "slug": "craig.gall",
                "type": "NORMAL",
                "links": {
                  "self": [
                    {
                      "href": "https://stash.blackline.corp/users/craig.gall"
                    }
                  ]
                }
              },
              "role": "REVIEWER",
              "status": "UNAPPROVED"
            },
            {
              "user": {
                "name": "praveen.sachdeva",
                "emailAddress": "praveen.sachdeva@blackline.com",
                "id": 6722,
                "displayName": "Praveen Sachdeva",
                "slug": "praveen.sachdeva",
                "type": "NORMAL",
                "links": {
                  "self": [
                    {
                      "href": "https://stash.blackline.corp/users/praveen.sachdeva"
                    }
                  ]
                }
              },
              "role": "REVIEWER",
              "status": "UNAPPROVED"
            }]
        }
        response = requests.post(url, json=data, headers=HEADERS)
        print("Response Status Code:", response.status_code)  # Add this line for debugging
        print("Response Content:", response.content)  # Add this line for debugging
        response.raise_for_status()
        pr = response.json()
        print(f'Pull request created: {pr["links"]["self"][0]["href"]}')
    
    if __name__ == "__main__":
        # Clone the repository
        run_command(f'git clone ssh://git@stash.blackline.corp:7999/tfm/root-mssql.git')
        os.chdir(REPO_SLUG)
        print(os.getcwd())
        
        # Create a new branch and update the variable
        create_branch()
        update_variable()
        
        # Push the new branch and create a pull request
        push_branch()
        create_pull_request()
