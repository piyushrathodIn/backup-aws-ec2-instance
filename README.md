EC2 Backup Script

This Python script performs automatic periodic backups of EC2 instances in AWS. The script uses the AWS SDK for Python (boto3) to connect to the AWS API, where it lists all the running EC2 instances in a specified region. It then creates a snapshot of each instance's EBS volumes and tags them with a timestamp to make them easily identifiable.

Features
# Automatic periodic backups of EC2 instances
# Uses AWS SDK for Python (boto3)
# Customizable backup schedule (daily, weekly, monthly)
# Exclusion of specific instances or volumes from backup process

Usage
# the repository
# Install the required packages: pip install -r requirements.txt
# Configure the AWS credentials in config.py
# Customize the backup schedule and exclusions in config.py
# Run the script: python app.py
# Note: This script can be scheduled to run automatically using a tool like cron or AWS CloudWatch Events.
