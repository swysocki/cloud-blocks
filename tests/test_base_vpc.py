from troposphere.ec2 import VPC, Route, RouteTable, Subnet, \
    SubnetRouteTableAssociation, InternetGateway, \
    VPCGatewayAttachment

from aws import base_vpc

import unittest
import warnings
import sys
import os

sys.path.append(os.path.abspath('..'))


class TestBaseVPC(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cidr = '1.0.0.0/16'
        cls.app_name = 'my-app-name'
        cls.region = 'us-east-1'
        cls.vpc_obj = base_vpc.vpc(cls.cidr, cls.app_name)
        cls.rt_obj = base_vpc.route_table(cls.app_name, cls.vpc_obj)
        cls.sbnt_list = base_vpc.subnets(cls.region,
                                         cls.cidr,
                                         cls.vpc_obj,
                                         cls.app_name)
        cls.igw = base_vpc.internet_gw(cls.app_name)
        cls.gw_attach = base_vpc.gateway_attach(cls.vpc_obj, cls.igw)
        cls.def_route = base_vpc.default_route(cls.igw,
                                               cls.rt_obj,
                                               cls.gw_attach)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_vpc(self):
        self.assertIsInstance(self.vpc_obj, VPC)

    def test_route_table(self):
        self.assertIsInstance(self.rt_obj, RouteTable)

    def test_subnet(self):
        for item in self.sbnt_list:
            self.assertIsInstance(item, Subnet)

    def test_subnet_assc(self):
        subnet_assc = base_vpc.subnet_assc(self.sbnt_list, self.rt_obj)
        for item in subnet_assc:
            self.assertIsInstance(item, SubnetRouteTableAssociation)

    def test_internet_gw(self):
        self.assertIsInstance(self.igw, InternetGateway)

    def test_gateway_attach(self):
        self.assertIsInstance(self.gw_attach, VPCGatewayAttachment)

    def test_default_route(self):
        self.assertIsInstance(self.def_route, Route)

    def test_build(self):
        warnings.simplefilter("ignore")
        res_list = base_vpc.build(self.app_name, self.region, self.cidr)
        self.assertIsNotNone(res_list)
        self.assertTrue(any(isinstance(x, VPC) for x in res_list))
        self.assertTrue(any(isinstance(x, RouteTable) for x in res_list))
        self.assertTrue(any(isinstance(x, Subnet) for x in res_list))
        self.assertTrue(any(isinstance(x, SubnetRouteTableAssociation)
                            for x in res_list))
        self.assertTrue(any(isinstance(x, InternetGateway) for x in res_list))
        self.assertTrue(any(isinstance(x, VPCGatewayAttachment)
                            for x in res_list))
        self.assertTrue(any(isinstance(x, Route) for x in res_list))


if __name__ == "__main__":
    unittest.main()
