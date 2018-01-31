import boto3
import logging


CLIENT = boto3.client('ec2')

def get_ubuntu_ami(release):
    ''' Returns newest Ubuntu AMI ID

    Params:
        release: Ubuntu Release name (trusty, xenial, etc.)
    Returns:
        AMI_ID: the AWS AMI identification code
    '''
    logging.info('Searching AWS for the most recent Ubuntu %s AMI', release)
    response = CLIENT.describe_images(
        Owners=['099720109477'],
        Filters=[
            {'Name': 'name', 'Values': ['ubuntu/images/hvm-ssd/ubuntu-'+release+'*']},
            {'Name': 'root-device-type', 'Values': ['ebs']}
        ]
    )
    if not response['Images']:
        logging.error('No search results for Ubuntu "%s"', release)
    elif response['ResponseMetadata']['HTTPStatusCode'] != 200:
        logging.error('Error Querying AWS %s', response['ResponseMetadata']['HTTPStatusCode'])
    else:
        ami_newest = sorted([image['Name'] for image in response['Images']], reverse=True)[0]
        ami_id = next((item['ImageId'] for item in response['Images'] if item['Name'] == ami_newest))
        return ami_id

if __name__ == '__main__':
    ami = get_ubuntu_ami('trusty')
    print(ami)
