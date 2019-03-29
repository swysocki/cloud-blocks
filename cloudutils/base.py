'''
General utitlity module for working with AWS Cloud Formation
configuration files

'''
import ipaddress
import boto3


def get_availability_zones(region):
    ''' Return a list of AZs in specified region '''
    ec2 = boto3.client('ec2', region_name=region)
    zones = ec2.describe_availability_zones()['AvailabilityZones']
    return [x['ZoneName'] for x in zones]


def create_subnets(supernet, subnet_count):
    ''' Generate subnet and mask based on supernet

    Breaks a class B (/16) into multiple class C (/24) subnets

    supernet:
    subnet_count:

    returns:
        list of subnets with prefix length

    '''
    prefix_length = 24
    subnet_list = list(
        ipaddress.ip_network(supernet).subnets(
            new_prefix=prefix_length))[0:subnet_count]

    return [x.with_prefixlen for x in subnet_list]
