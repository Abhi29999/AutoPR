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
