import unittest
import tempfile
import sys
import os
import subprocess

sys.path.append(os.path.abspath('..'))

from troposphere import Template
from aws import base_vpc

class TestBaseVPCCFN(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.TEMPLATE = Template()
        cls.VPC = base_vpc.build('testing-app,', 'us-east-1', '1.0.0.0/16')
    
    def test_vpc_cfn(self):
        for resource in self.VPC:
            self.TEMPLATE.add_resource(resource)
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as fp:
            fp.write(self.TEMPLATE.to_yaml())
            fp.close()
            ret = subprocess.run(['cfn-lint', 'validate', fp.name], check=True)
            self.assertEqual(ret.returncode, 0)
            os.unlink(fp.name)

if __name__ == "__main__":
    unittest.main()