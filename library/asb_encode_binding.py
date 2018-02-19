#!/usr/bin/python

ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: asb_encode_binding
short_description: Encodes binding fields for Ansible Service Broker
description:
     - Takes a dictionary of fields and makes them available to Ansible Service Broker
       to read and create a binding when running the action (provision, bind, etc)
notes: []
requirements: []
author:
    - "Red Hat, Inc."
options:
  fields:
    description:
      - 'dictionary of key/value pairs to encode for a binding.  Keys will become the injected environment variables.'
    required: true
    default: {}
 env:
        - Set via the downward API on the APB Pod
        - name: POD_NAME
          valueFrom:
            fieldRef:
              fieldPath: metadata.name
        - name: POD_NAMESPACE
          valueFrom:
            fieldRef:
              fieldPath: metadata.namespace    
'''

EXAMPLES = '''
- name: encode bind credentials
  asb_encode_binding:
    fields:
      POSTGRESQL_HOST: postgresql
      POSTGRESQL_PORT: 5432
      POSTGRESQL_USER: "{{ postgresql_user }}"
      POSTGRESQL_PASSWORD: "{{ postgresql_password }}"
      POSTGRESQL_DATABASE: "{{ postgresql_database }}"
'''
RETURN = '''
encoded_fields:
    description: string containing encoded fields
    returned: success
    type: string
    sample: eyJURVNUX1ZBUl8xIjogInRlc3QgdmFsdWUgMSIsICJUZXN0VmFsdWUyIjogMn0=
'''

import json
import base64
import os
from ansible.module_utils.basic import AnsibleModule
try:
    from kubernetes import client, config
    config.load_kube_config()
    api = client.CoreV1Api()
except Exception as error:
    ansible_module.fail_json(msg="Error attempting to load kubernetes client: {}".format(error))

ENCODED_BINDING_PATH = "/var/tmp/bind-creds"
ENV_NAME = "POD_NAME"
ENV_NAMESPACE = "POD_NAMESPACE"


def main():

    argument_spec = dict(
        fields=dict(required=True, type='dict')
    )

    ansible_module = AnsibleModule(argument_spec=argument_spec)

    try:
        fields_json = json.dumps(ansible_module.params['fields'])
        encoded_fields = base64.b64encode(fields_json)
    except Exception as error:
        ansible_module.fail_json(msg="Error attempting to encode binding: {}".format(error))

    try:
        name = os.environ[ENV_NAME]
        namespace = os.environ[ENV_NAMESPACE]
    except Exception as error:
        ansible_module.fail_json(msg="Error attempting to get name/namespace from environment: {}".format(error))

    try:
	api.create_namespaced_secret(
	    namespace=namespace,
	    body=client.V1Secret(
		metadata=client.V1ObjectMeta(name=name),
		data={"fields": encoded_fields}
	    )
	)
    except Exception as error:
        ansible_module.fail_json(msg="Error attempting to create binding secret: {}".format(error))

    ansible_module.exit_json(changed=True, encoded_fields=encoded_fields)


if __name__ == '__main__':
    main()
