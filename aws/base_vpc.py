from troposphere import Tags, Ref
from troposphere.ec2 import VPC, RouteTable, Subnet, \
    SubnetRouteTableAssociation
import utils

def create_vpc(cidr_block, tag_app_name, resources):
    vpc = VPC(
        'BaseVpc',
        CidrBlock=cidr_block,
        EnableDnsSupport=True,
        EnableDnsHostnames=True,
        InstanceTenancy="default",
        Tags=Tags(
            Name=tag_app_name+"-vpc"
        )
    )
    resources.append(vpc)
    return resources

def route_table(tag_app_name, resources):
    vpc_obj = [r for r in resources if type(r) == VPC]
    resources.append(
        RouteTable(
            "RouteTable",
            VpcId=Ref(vpc_obj),
            Tags=Tags(
                Name=tag_app_name+"-rt-1"
            )
        )
    )
    return resources

def subnets(region, cidr_block, resources, tag_app_name=None):
    azs = utils.get_availability_zones(region)
    subnet_list = utils.create_subnets(cidr_block, len(azs))
    vpc = [r for r in resources if type(r) == VPC]
    rt = [r for r in resources if type(r) == RouteTable]
    for idx, sbnt in enumerate(subnet_list):
        sbnt_obj = Subnet(
            'Subnet'+str(idx+1),
            CidrBlock=sbnt,
            MapPublicIpOnLaunch=True,
            VpcId=Ref(vpc),
            Tags=Tags(
                Name=tag_app_name+"-sbnt-"+str(idx+1)
            )
        )
        sbnt_assc_obj = SubnetRouteTableAssociation(
            'SubnetAssociation'+str(idx+1),
            SubnetId=Ref(sbnt_obj),
            RouteTableId=Ref(rt)
        )
        resources.append(sbnt_obj)
        resources.append(sbnt_assc_obj)

def create(app_name, region, cidr):
    resource_list = []
    create_vpc(cidr, app_name, resource_list)
    route_table(app_name, resource_list)
    subnets(region, cidr, resource_list, app_name)

    return resource_list

if __name__ == "__main__":
    APP = 'my-app'
    REGION = "us-east-1"
    CIDR = "10.1.0.0/16"
    RES = create(APP, REGION, CIDR)
    print(RES)
