from troposphere import Template, Tags, Ref
from troposphere.ec2 import VPC, Subnet, InternetGateway, \
    NatGateway, Route, RouteTable, VPCGatewayAttachment, \
    SubnetRouteTableAssociation

import utils

class SimpleVPC(object):
    """ General Purpose VPC """
    def __init__(self, app_name, region, cidr_block):
        """ Initialize """
        self._app_name = app_name
        self._region = region
        self._cidr_block = cidr_block
        self._vpc = None
        self._route_table = None
        self._subnets = []
        self.resources = []

        self._init_full()
        self.template = Template()

    def build_template(self):
        """ builds CFn template from current resources """
        pass

    def _init_full(self):
        self._create_vpc()
        self._create_subnets()
        self._create_route_table()
        self._create_subnet_assc()

    def _create_vpc(self):
        """ creates troposphere VPC resource """
        self.resources.append(
            VPC(
                'simpleVPC', #CFN resource name
                CidrBlock=self._cidr_block,
                EnableDnsSupport=True,
                EnableDnsHostnames=True,
                InstanceTenancy="default",
                Tags=Tags(
                    Name=self._app_name+"-vpc-01" # generated name (<app>-<resource>-<index>)
                )
            )
        )

    def _create_subnets(self):
        """ associate subnets to VPC """
        # check that self.resources contains a troposphere.ec2.vpc object
        azs = utils.get_availability_zones(self._region)
        subnets = utils.create_subnets(self._cidr_block, len(azs))
        for idx, sbnt in enumerate(subnets):
            subnet_obj = Subnet(
                'Subnet'+str(idx+1),
                CidrBlock=sbnt,
                MapPublicIpOnLaunch=False,
                VpcId=Ref(self._vpc),
                Tags=Tags(
                    Name=self._app_name+'-sbnt-'+str(idx+1)
                )
            )
            self.resources.append(subnet_obj)
                
    def _create_route_table(self):
        """ create a public route table """
        self.resources.append(
                    RouteTable(
                    'PublicRouteTable',
                    VpcId=Ref(self._vpc),
                    Tags=Tags(
                        Name=self._app_name+"-rt-tbl"
                    )
                )
        )

    def _create_subnet_assc(self):
        """ associate subnets with public route table """
        for idx, subnet in enumerate(self.subnets):
            assc_obj = SubnetRouteTableAssociation(
                'PubSubnetAssc'+str(idx+1),
                SubnetId=Ref(subnet),
                RouteTableId=Ref(self.route_table)
            )
            self.subnet_assc.append(assc_obj)
    
    def print_template(self):
        """ print json of template """
        print(self.template.to_json())

if __name__ == "__main__":
    VPC = SimpleVPC('my-app', 'us-east-1', "10.101.0.0/16")
    VPC.print_template()