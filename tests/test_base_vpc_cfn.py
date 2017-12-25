
import tempfile
import sys
import os
import subprocess

sys.path.append(os.path.abspath('..'))

from troposphere import Template
from aws import base_vpc

if __name__ == "__main__":
    TEMPLATE = Template()
    VPC = base_vpc.build('testing-app', 'us-east-1', '1.0.0.0/16')
    for resource in VPC:
        TEMPLATE.add_resource(resource)
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as fp:
        fp.write(TEMPLATE.to_yaml())
        fp.close()
        subprocess.run(['cfn-lint', 'validate', fp.name], shell=True)
        os.unlink(fp.name)
