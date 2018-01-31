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

