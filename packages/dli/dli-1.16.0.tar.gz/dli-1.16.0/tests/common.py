import json
import logging
from random import randint
import os
import random
import string
import time
import unittest
import uuid
import jwt
from unittest.mock import patch

import requests
from urllib import parse

from moto.s3.exceptions import BucketAlreadyExists

from dli.client import builders, session
from tests import localstack_helper

def _get_token(secret: str) -> str:
    # make sure the user matches the db_state.sql
    token_data = {
        "datalake": {
            "user_id": "68eda64b-f933-473b-b3ef-4d8e22baa648",
            "organisation_id": "9516c0ba-ba7e-11e9-8b34-000c6c0a981f"
        },
        "name": "w molicki",
        "email": "wmolicki@qa.com",
        "sub": "wmolicki@qa.com",
        "azp": "datalake-catalogue-dev",
        "aud": "datalake-catalogue-dev",
        "iat": 1624958089,
        "exp": 1656580489
    }

    token_encoded = jwt.encode(token_data, secret)
    if isinstance(token_encoded, bytes):
        return token_encoded.decode('utf-8')
    else:
        return token_encoded


token = _get_token('secret')


class SdkIntegrationTestCase(unittest.TestCase):
    """
    Helper TestCase to test against a local docker container running the datacat api.
    To run these locally, run `docker-compose up` on the root directory
    """

    @staticmethod
    def random_with_N_digits(n):
        range_start = 10 ** (n - 1)
        range_end = (10 ** n) - 1
        return randint(range_start, range_end)

    @patch("dli.client.dli_client.Session._get_web_auth_key", lambda self: token)
    @patch("dli.client.dli_client.AnalyticsHandler", lambda self: None)
    def setUp(self):

        self.headers = {
            'Content-type': 'application/json',
            'Authorization': 'Bearer {}'.format(token),
            # 'Cookie': 'oidc_id_token=' + token
        }
        self.root_url = os.environ.get("DATA_LAKE_INTERFACE_URL")
        self.root_identity_url = os.environ.get("DATA_LAKE_ACCOUNTS_URL")

        self.client = self.create_session()
        self.s3 = []
        self.aws_account_id = SdkIntegrationTestCase.random_with_N_digits(5)  # N.B. this needs to match the JWT, else 500
        self.register_aws_account(self.aws_account_id)

        self.s3_client = localstack_helper.get_s3_client()

    def create_package(self, name, access="Restricted", **kwargs):
        payload = {
            "data": {
                "attributes": {
                    "name": name + "_" + str(uuid.uuid4()),
                    "description": f"asd",
                    "keywords": ['testing'],
                    "topic": 'Climate',
                    "access": access,
                    "terms_and_conditions": 'There are no terms and conditions',
                    "publisher": 'b30a3e2c-ad7e-11eb-b02d-377b10141544',
                    "suborganisation_id": '6a0cd22b-2ad5-4440-9b70-c7a13d5f0a68'
                }
            }
        }

        payload = {k: v for k, v in payload.items() if v is not None}
        response = requests.post(parse.urljoin(self.root_url, "__api_v2/packages"),
            headers=self.headers,
            json=payload
        )

        return response.json()["data"]["id"]

    def dataset_builder(self, package_id, dataset_name, **kwargs):
        arguments = dict(kwargs)
        data_preview_type = arguments.pop('data_preview_type', 'NONE')
        default_short_code = ''.join(random.choices(
            string.ascii_letters + string.digits, k=10
        ))
        short_code = arguments.pop('short_code', default_short_code)
        return builders.DatasetBuilder(
            package_id=package_id,
            name=dataset_name,
            description='a testing dataset',
            content_type='Structured',
            data_format='CSV',
            publishing_frequency='Daily',
            taxonomy=[],
            data_preview_type=data_preview_type,
            short_code=short_code,
            **arguments
        )

    def register_s3_dataset(self, package_id, dataset_name, bucket_name, prefix="prefix"):
        self._setup_bucket_and_prefix(bucket_name, prefix)
        return self.client.register_dataset(
            self.dataset_builder(package_id, dataset_name).with_external_s3_storage(
                bucket_name,
                self.aws_account_id,
                prefix
            )
        )

    def _setup_bucket_and_prefix(self, bucket_name, prefix):
        # API checks whether DataLake can access S3 bucket at prefix. If dataset is registered with S3 location
        # we must create a fake one in localstack.
        def cleanup_bucket():
            for object_to_delete in s3_client.list_objects(Bucket=bucket_name)['Contents']:
                s3_client.delete_objects(Bucket=bucket_name, Delete={"Objects": [{"Key": object_to_delete['Key']}]})
            s3_client.delete_bucket(Bucket=bucket_name)

        s3_client = self.s3_client
        try:
            s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': 'eu-west-1'})
        except BucketAlreadyExists:
            cleanup_bucket()
            s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': 'eu-west-1'})

        s3_client.put_object(
            Bucket=bucket_name,
            # Ensure key ends in a slash to signify it's a directory
            Key=prefix.rstrip('/') + '/',
            Body=""
        )


        self.addCleanup(cleanup_bucket)

    def create_session(self):
        return session._start_session(self.root_url)

    def register_aws_account(self, aws_account_id):
        response = requests.post(
            parse.urljoin(self.root_url, "__api_v2/aws_accounts"),
            headers={
                'Authorization': 'Bearer {}'.format(token),
                'Content-type': 'application/json',
            },
            data=json.dumps({
                'data': {
                    'attributes': {
                        "vendor_aws_account_id": str(aws_account_id),
                        "vendor_aws_account_name": str(aws_account_id),
                        "aws_region": "eu-west-1",
                        "aws_role_arn": 'arn:aws:iam::000000000001:user/root',
                        "organisation_id": '9516c0ba-ba7e-11e9-8b34-000c6c0a981f'
                    }
                }
            })
        )


        # get our user group
        ug = requests.get(
            parse.urljoin(self.root_identity_url,"__api_v2/user_groups/"),
            headers={
                'Authorization': 'Bearer {}'.format(token),
                'Content-type': 'application/json',
            }
        )

        print(ug.json())
        ug = ug.json()["data"][0]['id']

        try:
            # Must add our user's usergroup to the aws role to be able to use it
            add_user_to_aws_account = requests.post(
                parse.urljoin(self.root_identity_url, f"__api_v2/user_groups/{ug}/roles"),
                headers={
                    'Authorization': 'Bearer {}'.format(token),
                    'Content-type': 'application/json',
                },
                json={
                    'owner_type': 'aws-accounts',
                    'owner_id': response.json()['data']['id'],
                    'role': 'aws-account-user'
                }
            )
        except KeyError as e:
            raise Exception(response.json())

        # this will not be reached in the case of fatal :/
        assert(response.status_code == 201 or response.status_code == 422) #create or exists

    def patch_upload_files_to_s3(self, files, location, tr=None, r=None):
        result = []
        for f in files:
            path = location + os.path.basename(f)
            self.s3.append(path)
            result.append({"path": "s3://" + path})
        return result

    def assert_page_count_is_valid_for_paginated_resource_actions(self, func):
        with self.assertRaises(ValueError):
            func(-1)
        with self.assertRaises(ValueError):
            func(0)
        with self.assertRaises(ValueError):
            func("test")
