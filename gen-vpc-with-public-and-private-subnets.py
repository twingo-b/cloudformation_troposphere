from troposphere import Base64, FindInMap, GetAtt, Join, Output
from troposphere import Parameter, Ref, Tags, Template
from troposphere.cloudfront import Distribution, DistributionConfig
from troposphere.cloudfront import Origin, DefaultCacheBehavior
from troposphere.ec2 import PortRange
from troposphere.ec2 import Route
from troposphere.ec2 import SecurityGroupIngress
from troposphere.ec2 import RouteTable
from troposphere.ec2 import EIP
from troposphere.ec2 import SecurityGroup
from troposphere.ec2 import SubnetRouteTableAssociation
from troposphere.ec2 import VPCGatewayAttachment
from troposphere.ec2 import Subnet
from troposphere.ec2 import InternetGateway
from troposphere.ec2 import Instance
from troposphere.ec2 import VPC

t = Template()

t.add_description("""\
AWS CloudFormation Sample Template VPC with Public and Private Subnets\
""")

# params
vpccidr_param = t.add_parameter(Parameter(
    "VpcCidr",
    Description="VPC CIDR",
    Default="10.0.0.0/16",
    Type="String",
    ))

publicsubnetcidr_param = t.add_parameter(Parameter(
    "PublicSubnetCidr",
    Description="PublicSubnet CIDR",
    Default="10.0.0.0/24",
    Type="String",
    ))

privatesubnetcidr_param = t.add_parameter(Parameter(
    "PrivateSubnetCidr",
    Description="PrivateSubnet CIDR",
    Default="10.0.1.0/24",
    Type="String",
    ))

availavilityzone_param = t.add_parameter(Parameter(
    "AvailabilityZone",
    Description="VPC AvailabilityZone",
    Default="ap-northeast-1a",
    Type="String",
    ))

natinstancetype_param = t.add_parameter(Parameter(
    "NatInstanceType",
    Description="NAT InstanceType",
    Default="t2.micro",
    Type="String",
    ))

natimageid_param = t.add_parameter(Parameter(
    "NatImageId",
    Description="NAT ImageId",
    Default="ami-27d6e626",
    Type="String",
    ))

natkeyname_param = t.add_parameter(Parameter(
    "NatKeyName",
    Description="NAT KeyName",
    Default="gameday",
    Type="String",
    ))

# VPC with Public and Private Subnets
DefaultPrivateRoute = t.add_resource(Route(
    "DefaultPrivateRoute",
    InstanceId=Ref("Nat"),
    DestinationCidrBlock="0.0.0.0/0",
    RouteTableId=Ref("PrivateRouteTable"),
))

NatHTTPIngress = t.add_resource(SecurityGroupIngress(
    "NatHTTPIngress",
    ToPort="80",
    FromPort="80",
    IpProtocol="tcp",
    GroupId=Ref("NatSG"),
    CidrIp=Ref(privatesubnetcidr_param),
))

PublicRouteTable = t.add_resource(RouteTable(
    "PublicRouteTable",
    VpcId=Ref("VPC"),
    Tags=Tags(
        Name=Join("",[Ref("AWS::StackName"),"-public"]),
    )
))

NatEIP = t.add_resource(EIP(
    "NatEIP",
    InstanceId=Ref("Nat"),
    Domain="vpc",
))

NatSG = t.add_resource(SecurityGroup(
    "NatSG",
    VpcId=Ref("VPC"),
    GroupDescription="Security group for NAT host.",
    Tags=Tags(
        Name=Join("",[Ref("AWS::StackName"),"-nat"]),
    )
))

PublicAssociation = t.add_resource(SubnetRouteTableAssociation(
    "PublicAssociation",
    SubnetId=Ref("PublicSubnet"),
    RouteTableId=Ref(PublicRouteTable),
))

PrivateRouteTable = t.add_resource(RouteTable(
    "PrivateRouteTable",
    VpcId=Ref("VPC"),
    Tags=Tags(
        Name=Join("",[Ref("AWS::StackName"),"-private"]),
    )
))

PrivateRouteAssociation = t.add_resource(SubnetRouteTableAssociation(
    "PrivateRouteAssociation",
    SubnetId=Ref("PrivateSubnet"),
    RouteTableId=Ref(PrivateRouteTable),
))

NatSSHIngress = t.add_resource(SecurityGroupIngress(
    "NatSSHIngress",
    ToPort="22",
    FromPort="22",
    IpProtocol="tcp",
    GroupId=Ref(NatSG),
    CidrIp="0.0.0.0/0",
))

VPCGatewayAttachment = t.add_resource(VPCGatewayAttachment(
    "VPCGatewayAttachment",
    VpcId=Ref("VPC"),
    InternetGatewayId=Ref("InternetGateway"),
))

NatHTTPSIngress = t.add_resource(SecurityGroupIngress(
    "NatHTTPSIngress",
    ToPort="443",
    FromPort="443",
    IpProtocol="tcp",
    GroupId=Ref(NatSG),
    CidrIp=Ref(privatesubnetcidr_param),
))

PublicSubnet = t.add_resource(Subnet(
    "PublicSubnet",
    VpcId=Ref("VPC"),
    AvailabilityZone=Ref(availavilityzone_param),
    CidrBlock=Ref(publicsubnetcidr_param),
    Tags=Tags(
        Name=Join("",[Ref("AWS::StackName"),"-public"]),
    )
))

PrivateSubnet = t.add_resource(Subnet(
    "PrivateSubnet",
    VpcId=Ref("VPC"),
    AvailabilityZone=Ref(availavilityzone_param),
    CidrBlock=Ref(privatesubnetcidr_param),
    Tags=Tags(
        Name=Join("",[Ref("AWS::StackName"),"-private"]),
    )
))

InternetGateway = t.add_resource(InternetGateway(
    "InternetGateway",
    Tags=Tags(
        Name=Ref("AWS::StackName"),
    )
))

DefaultPublicRoute = t.add_resource(Route(
    "DefaultPublicRoute",
    GatewayId=Ref(InternetGateway),
    DestinationCidrBlock="0.0.0.0/0",
    RouteTableId=Ref(PublicRouteTable),
))

Nat = t.add_resource(Instance(
    "Nat",
    SourceDestCheck="false",
    SecurityGroupIds=[Ref(NatSG)],
    KeyName=Ref(natkeyname_param),
    SubnetId=Ref(PublicSubnet),
    ImageId=Ref(natimageid_param),
    InstanceType=Ref(natinstancetype_param),
    Tags=Tags(
        Name=Join("",[Ref("AWS::StackName"),"-nat"]),
    )
))

VPC = t.add_resource(VPC(
    "VPC",
    EnableDnsSupport="true",
    CidrBlock=Ref(vpccidr_param),
    EnableDnsHostnames="true",
    Tags=Tags(
        Name=Ref("AWS::StackName"),
    )
))

print(t.to_json())
