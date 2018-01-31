# Cloud-blocks : Composable Templates to build cloud resources written in Python.

Because YAML/JSON shouldn't be written by hand!

## Examples 

### Build a VPC in AWS

``` python
from aws import base_vpc
from troposphere import Template

TEMPLATE = Template()
VPC = base_vpc.build('my-app-name', 'us-east-1', '1.0.0.0/16')
for resource in VPC:
    TEMPLATE.add_resource(resource)

with open("cfn_template.yml", mode="w") as f:
    f.write(TEMPLATE.to_yaml())
```

Template will look like:

``` yaml
Resources:
  BaseVpc:
    Properties:
      CidrBlock: 1.0.0.0/16
      EnableDnsHostnames: 'true'
      EnableDnsSupport: 'true'
      InstanceTenancy: default
      Tags:
        - Key: Name
          Value: my-app-name-vpc
    Type: AWS::EC2::VPC
  DefaultRoute:
    DependsOn: VpcGatewayAttachment
    Properties:
      DestinationCidrBlock: 0.0.0.0/0
      GatewayId: !Ref 'InternetGateway'
      RouteTableId: !Ref 'RouteTable'
    Type: AWS::EC2::Route
  InternetGateway:
    Properties:
      Tags:
        - Key: Name
          Value: my-app-name-igw
    Type: AWS::EC2::InternetGateway
  RouteTable:
    Properties:
      Tags:
        - Key: Name
          Value: my-app-name-rt-1
      VpcId: !Ref 'BaseVpc'
    Type: AWS::EC2::RouteTable
  Subnet1:
    Properties:
      CidrBlock: 1.0.0.0/24
      MapPublicIpOnLaunch: 'true'
      Tags:
        - Key: Name
          Value: my-app-name-sbnt-1
      VpcId: !Ref 'BaseVpc'
    Type: AWS::EC2::Subnet
  Subnet2:
    Properties:
      CidrBlock: 1.0.1.0/24
      MapPublicIpOnLaunch: 'true'
      Tags:
        - Key: Name
          Value: my-app-name-sbnt-2
      VpcId: !Ref 'BaseVpc'
    Type: AWS::EC2::Subnet
  Subnet3:
    Properties:
      CidrBlock: 1.0.2.0/24
      MapPublicIpOnLaunch: 'true'
      Tags:
        - Key: Name
          Value: my-app-name-sbnt-3
      VpcId: !Ref 'BaseVpc'
    Type: AWS::EC2::Subnet
  Subnet4:
    Properties:
      CidrBlock: 1.0.3.0/24
      MapPublicIpOnLaunch: 'true'
      Tags:
        - Key: Name
          Value: my-app-name-sbnt-4
      VpcId: !Ref 'BaseVpc'
    Type: AWS::EC2::Subnet
  Subnet5:
    Properties:
      CidrBlock: 1.0.4.0/24
      MapPublicIpOnLaunch: 'true'
      Tags:
        - Key: Name
          Value: my-app-name-sbnt-5
      VpcId: !Ref 'BaseVpc'
    Type: AWS::EC2::Subnet
  Subnet6:
    Properties:
      CidrBlock: 1.0.5.0/24
      MapPublicIpOnLaunch: 'true'
      Tags:
        - Key: Name
          Value: my-app-name-sbnt-6
      VpcId: !Ref 'BaseVpc'
    Type: AWS::EC2::Subnet
  SubnetAssocation1:
    Properties:
      RouteTableId: !Ref 'RouteTable'
      SubnetId: !Ref 'Subnet1'
    Type: AWS::EC2::SubnetRouteTableAssociation
  SubnetAssocation2:
    Properties:
      RouteTableId: !Ref 'RouteTable'
      SubnetId: !Ref 'Subnet2'
    Type: AWS::EC2::SubnetRouteTableAssociation
  SubnetAssocation3:
    Properties:
      RouteTableId: !Ref 'RouteTable'
      SubnetId: !Ref 'Subnet3'
    Type: AWS::EC2::SubnetRouteTableAssociation
  SubnetAssocation4:
    Properties:
      RouteTableId: !Ref 'RouteTable'
      SubnetId: !Ref 'Subnet4'
    Type: AWS::EC2::SubnetRouteTableAssociation
  SubnetAssocation5:
    Properties:
      RouteTableId: !Ref 'RouteTable'
      SubnetId: !Ref 'Subnet5'
    Type: AWS::EC2::SubnetRouteTableAssociation
  SubnetAssocation6:
    Properties:
      RouteTableId: !Ref 'RouteTable'
      SubnetId: !Ref 'Subnet6'
    Type: AWS::EC2::SubnetRouteTableAssociation
  VpcGatewayAttachment:
    Properties:
      InternetGatewayId: !Ref 'InternetGateway'
      VpcId: !Ref 'BaseVpc'
    Type: AWS::EC2::VPCGatewayAttachment
```