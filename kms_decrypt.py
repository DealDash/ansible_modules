#!/usr/bin/python
import base64

DOCUMENTATION = '''
short_description: Decrypt a secret that was generated by KMS
description:
  - This module decrypts the given secret using AWS KMS, and returns it as the Plaintext property
version_added: null
author: Ben Bridts
notes:
  - Make sure you read http://docs.aws.amazon.com/kms/latest/developerguide/control-access.html to learn how to restrict
    access to your keys
requirements:
  - the boto3 python package
options:
  aws_secret_key:
    description:
      - AWS secret key. If not set then the value of the AWS_SECRET_KEY environment variable is used.
    required: false
    default: null
    aliases: [ 'ec2_secret_key', 'secret_key' ]
    version_added: "1.5"
  aws_access_key:
    description:
      - AWS access key. If not set then the value of the AWS_ACCESS_KEY environment variable is used.
    required: false
    default: null
    aliases: [ 'ec2_access_key', 'access_key' ]
    version_added: "1.5"
  region:
    description:
      - The AWS region to use. If not specified then the value of the EC2_REGION environment variable, if any, is used.
    required: false
    aliases: ['aws_region', 'ec2_region']
    version_added: "1.5"
  secret:
    description:
      - The encrypted string you want to decode
    required: false
    default: CAT
'''

EXAMPLES = '''
- name: Decrypt secret
  kms_decrypt:
    secret: "{{ secret }}"
  register: result
  delegate_to: 127.0.0.1
- name: Show plaintext
  debug: var=result.plaintext
  delegate_to: 127.0.0.1
'''

import sys

try:
    import boto3
except ImportError:
    print "failed=True msg='boto3 required for this module'"
    sys.exit(1)


def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(
        secret=dict(required=True),
    ))

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    secret = module.params.get('secret')
    secret = base64.decodestring(secret)

    client = boto3.client('kms')

    response = client.decrypt(
        CiphertextBlob=secret
    )

    status_code = response['ResponseMetadata']['HTTPStatusCode']
    if status_code != 200:
        module.fail_json(msg='Failed with http status code %s' % status_code)

    module.exit_json(changed=True, plaintext=response['Plaintext'], key_id=response['KeyId'])


from ansible.module_utils.basic import *
from ansible.module_utils.ec2 import *

main()
