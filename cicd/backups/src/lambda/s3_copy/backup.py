import logging
import json
import os
import datetime
import re
import subprocess

logger = logging.getLogger('s3_copy')
logger.setLevel(logging.DEBUG)

# Create a StreamHandler to print log messages to the console (stdout)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Add the console handler to the logger
logger.addHandler(console_handler)

# This adds our package location to the python path, it allows us to run the locally installed awscli 
os.environ['PYTHONPATH'] = f"{os.environ['PYTHONPATH']}:{os.environ['LAMBDA_TASK_ROOT']}" 
  
def handler(event, context):
  shell_cmds = []

  logger.info('Received event: {}'.format(json.dumps(event))) 
  
  # create a string based on the date to be used as a directory name in S3
  backup_date = datetime.datetime.now().strftime("%Y%m%d")

  # determine if this is the first backup of the week. Used in dir name as a quick
  # way to apply different lifecycle rules to weekly and daily backups
  if datetime.datetime.today().weekday() == 0:
    backup_freq = 'weekly'
  else :
    backup_freq = 'daily'

  shell_cmds.append( f"""python ./export_users.py
                           --user-pool-id {os.environ['USER_POOL_ID']}
                           --region {os.environ['AWS_REGION']}
                           -f /tmp/cognito_users.csv""" )

  shell_cmds.append(f"""python ./export_groups.py
                          --user-pool-id {os.environ['USER_POOL_ID']}
                          --region {os.environ['AWS_REGION']} > /tmp/cognito_groups.json""" )

  shell_cmds.append(f"""bin/aws s3 cp
                          --sse "aws:kms"
                          --storage-class "{os.environ['STORAGE_CLASS']}"
                          /tmp/cognito_users.csv s3://{os.environ['BACKUP_BUCKET']}/backup-{backup_freq}-{backup_date}/""" )

  shell_cmds.append(f"""bin/aws s3 cp
                          --sse "aws:kms"
                          --storage-class "{os.environ['STORAGE_CLASS']}"
                          /tmp/cognito_groups.json s3://{os.environ['BACKUP_BUCKET']}/backup-{backup_freq}-{backup_date}/""" )


  for command in shell_cmds:
    #collapse whitespace in the command string
    command = re.sub(r"\s+", " ", command)

    logger.info(f"running command: {command}")
  
    try:
      completed_process = subprocess.run(command, shell=True, check=True, capture_output=True)

      logger.info(f'Output:{completed_process.stdout.decode()}')

      if completed_process.stderr:  # only if there is an error message
          logger.error(completed_process.stderr.decode())

    except subprocess.CalledProcessError as e:
      logger.critical(e.stderr.decode())
    except Exception as e:
      logger.critical(f"An unexpected error occurred: {str(e)}")

    
# only used when testing locally
if __name__ == '__main__':
  handler({'dummy-event' : True}, {'dummy-context' : True})