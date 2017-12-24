import sys, os
sys.path.append(os.path.abspath(".."))

from troposphere import Template
from aws import base_vpc

if __name__ == "__main__":
    test_vpc = base_vpc.build('my-app', 'us-east-1', '10.1.0.0/16')
    test_template = Template()
    for r in test_vpc:
        test_template.add_resource(r)
    print(test_template.to_json())
