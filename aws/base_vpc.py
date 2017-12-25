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
    SubnetRouteTableAssociation, InternetGateway, \
    VPCGatewayAttachment
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
    """ creates a route table

    Params:
        tag_app_name: application name used to create AWS tag
        vpc_obj: troposphere.ec2.VPC object
    Returns:
        troposphere.ec2.RouteTable object
    """
    return RouteTable(
        "RouteTable",
        VpcId=Ref(vpc_obj),
        Tags=Tags(
            Name=tag_app_name+"-rt-1"
        )
    )

def subnets(region, cidr_block, vpc_obj, tag_app_name):
    """ creates AWS Subnets

    This function uses boto3 to enumerate the AZ's in a region and
    creates a subnet per AZ.  The initial cidr_block is a /16. Each
    Subnet will be a /24 of this supernet.

    Params:
        region: AWS region name ie: "us-east-1"
        cidr_block: /16 that individual /24 will be created from
        vpc_obj: troposphere.ec2.VPC object
        tag_app_name: application name used to create AWS tag
    Returns:
        subnet_resources: a list of troposphere.ec2.Subnet objects
    """
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
    """ associate subnets with route tables

    Params:
        subnet_list: a list of troposphere.ec2.Subnet objects
        rt_obj: troposphere.ec2.RouteTable object
    Returns:
        subnet_associations: a list of
            troposphere.ec2.SubnetRouteTableAssociation objects
    """
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

def internet_gw(tag_app_name):
    """ creates an Internet gateway

    Params:
        tag_app_name: application name used to create AWS tag
    Returns:
        troposphere.ec2.InternetGateway object
    """
    return InternetGateway(
        'InternetGateway',
        Tags=Tags(
            Name=tag_app_name+"-igw"
        )
    )

def gateway_attach(vpc_obj, gateway_obj):
    """ attaches an Internet gateway to a VPC

    Params:
        vpc_obj: troposphere.ec2.VPC object
        gateway_obj: troposphere.ec2.InternetGateway object
    Returns:
        troposphere.ec2.VPCGateAttachement object
    """
    return VPCGatewayAttachment(
        'VpcGatewayAttachment',
        VpcId=Ref(vpc_obj),
        InternetGatewayId=Ref(gateway_obj)
    )

def default_route(inet_gw, route_table, attachment):
    """ creates default route

    Params:
        inet_gw: troposphere.ec2.InternetGateway object
        route_table: troposphere.ec2.RouteTable object
        attachment: troposphere.ec2.VPCGatewayAttachment object
    Returns:
        troposphere.ec2.Route object
    """
    return Route(
        'DefaultRoute',
        DependsOn=attachment,
        DestinationCidrBlock='0.0.0.0/0',
        GatewayId=Ref(inet_gw),
        RouteTableId=Ref(route_table)
    )

def build(app_name, region, cidr):
    """ builds all base_vpc resources

    Params:
        app_name: Application short name
        region: AWS region title, ie: "us-east-1"
        cidr: /16 supernet
    Returns:
        resource_list: a list of troposphere.ec2.* objects that can be
            put in a troposphere Template object
    """
    resource_list = []

    # vpc
    b_vpc = vpc(cidr, app_name)
    resource_list.append(b_vpc)

    # route table
    b_rt = route_table(app_name, b_vpc)
    resource_list.append(b_rt)

    # subnets
    b_subnets = subnets(region, cidr, b_vpc, app_name)
    for sub in b_subnets:
        resource_list.append(sub)

    # subnet associations
    b_sbnt_assc = subnet_assc(b_subnets, b_rt)
    for sb_asc in b_sbnt_assc:
        resource_list.append(sb_asc)

    # internet gateway
    b_gateway = internet_gw(app_name)
    resource_list.append(b_gateway)

    # gateway attachment
    b_gw_assc = gateway_attach(b_vpc, b_gateway)
    resource_list.append(b_gw_assc)

    # default route
    b_route = default_route(b_gateway, b_rt, b_gw_assc)
    resource_list.append(b_route)

    return resource_list
