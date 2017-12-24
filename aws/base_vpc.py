""" Base VPC module

This creates a list of troposphere resource object that can be 
converted to a CloudFormation or combined with other resources
to make a larger CFn Stack.

resources created:
- VPC object
- a single route table
- a single subnet per availiblity zone
- subnet association for each subnet
- internet gateway
- default route
"""

from troposphere import Tags, Ref
from troposphere.ec2 import VPC, RouteTable, Subnet, \
    SubnetRouteTableAssociation
import utils

def vpc(cidr_block, tag_app_name):
    """ creates base VPC object

    Params:
        cidr_block: /16 subnet
        tag_app_name: application name used to create AWS tag
    Returns:
        troposphere.ec2.VPC object
    """

    return VPC(
        'BaseVpc',
        CidrBlock=cidr_block,
        EnableDnsSupport=True,
        EnableDnsHostnames=True,
        InstanceTenancy="default",
        Tags=Tags(
            Name=tag_app_name+"-vpc"
        )
    )

def route_table(tag_app_name, vpc_obj):
    """ creates a route table """
    return RouteTable(
        "RouteTable",
        VpcId=Ref(vpc_obj),
        Tags=Tags(
            Name=tag_app_name+"-rt-1"
        )
    )

def subnets(region, cidr_block, vpc_obj, tag_app_name):
    azs = utils.get_availability_zones(region)
    subnet_list = utils.create_subnets(cidr_block, len(azs))
    subnet_resources = []
    for idx, sbnt in enumerate(subnet_list):
        subnet_resources.append(
            Subnet(
                'Subnet'+str(idx+1),
                CidrBlock=sbnt,
                MapPublicIpOnLaunch=True,
                VpcId=Ref(vpc_obj),
                Tags=Tags(
                    Name=tag_app_name+"-sbnt-"+str(idx+1)
                )
            )
        )
    return subnet_resources

def subnet_assc(subnet_list, rt_obj):
    subnet_associations = []
    for idx, subnet in enumerate(subnet_list):
        subnet_associations.append(
            SubnetRouteTableAssociation(
                'SubnetAssocation'+str(idx+1),
                SubnetId=Ref(subnet),
                RouteTableId=Ref(rt_obj)
            )
        )
    return subnet_associations

def build(app_name, region, cidr):
    resource_list = []
    b_vpc = vpc(cidr, app_name)
    resource_list.append(b_vpc)
    
    b_rt = route_table(app_name, b_vpc)
    resource_list.append(b_rt)

    b_subnets = subnets(region, cidr, b_vpc, app_name)
    for sub in b_subnets:
        resource_list.append(sub)

    b_sbnt_assc = subnet_assc(b_subnets, b_rt)
    for sb_asc in b_sbnt_assc:
        resource_list.append(sb_asc)

    return resource_list

