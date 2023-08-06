import unittest

import ibm_boto3

from ibm_watson_machine_learning.helpers.connections import DataConnection, ContainerLocation, S3Location
from ibm_watson_machine_learning.utils.autoai.errors import WMLClientError
from ibm_watson_machine_learning.tests.utils import bucket_exists, is_cp4d, create_bucket
from ibm_watson_machine_learning.tests.autoai.svt.abstract_test_iris_wml_autoai_multiclass_connections import (
    AbstractTestAutoAIRemote)


@unittest.skipIf(is_cp4d(), "Supported only on CLOUD")
class TestAutoAIRemote(AbstractTestAutoAIRemote, unittest.TestCase):
    """
    The test can be run on CLOUD
    The test covers:
    - COS connection set-up
    - Saving data `iris.csv` to s3 connection
    - downloading training data from connection
    - downloading all generated pipelines to lale pipeline
    - deployment with lale pipeline
    - deployment deletion
    Connection used in test:
     - input: S3 connection pointing to COS.
     - output: ConnectedDataAsset pointing to COS.
    """

    def test_02_DataConnection_setup(self):
        TestAutoAIRemote.data_connection = DataConnection(
            location=ContainerLocation(path=self.data_cos_path
                                       ))

        TestAutoAIRemote.results_connection = DataConnection(
            location=ContainerLocation(path=self.results_cos_path))
        # TestAutoAIRemote.data_connection.write(data=self.data_location, remote_name=self.data_cos_path)

        self.assertIsNotNone(obj=TestAutoAIRemote.data_connection)
        self.assertIsNotNone(obj=TestAutoAIRemote.results_connection)

    def test_02a_read_saved_remote_data_before_fit(self):
        pass


if __name__ == '__main__':
    unittest.main()
