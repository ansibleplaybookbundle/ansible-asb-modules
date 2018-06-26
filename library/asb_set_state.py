#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: asb_set_state
short_description: Sets state in a ConfigMap
description:
     - Provides a secure method for allowing Service Bundle developers
       to set state during a Service Bundle action.
       Provided key, value pair is stored in a ConfigMap for later retrieval.
author:
    - "Red Hat, Inc."
options:
    key:
        description:
            - Unique key
        required: true
    value:
        description:
            - Literal value
        required: true
 env:
        # Set via the downward API on the APB Pod
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
- name: Set some example state
  asb_set_state:
    fields:
      key_one: "example-value-one"
      key_two: "example-value-two"
'''

import os

from ansible.module_utils.basic import AnsibleModule
try:
    from kubernetes import client, config
    from kubernetes.client.rest import ApiException
    HAS_K8_CLIENT = True
except ImportError as error:
    HAS_K8_CLIENT = False


ENV_NAME = 'POD_NAME'
ENV_NAMESPACE = 'POD_NAMESPACE'

def should_update(existing, new):
    if len(existing) < len(new):
        return True
    for key, value in new.items():
        if not existing.has_key(key):
            return True
        if value != existing[key]:
            return True
    return False


def run(module):
    try:
        name = os.environ[ENV_NAME]
        namespace = os.environ[ENV_NAMESPACE]
    except KeyError as e:
        module.fail_json(
            msg='Error attempting to get name/namespace from environment: {}'.format(e))

    config.load_kube_config()
    api = client.CoreV1Api()
    unparsed_data = module.params['fields']
    data = dict()

    for key, value in unparsed_data.items():
        if type(value) == str:
            data[key] = value
        else:
            try:
                str_val = str(value)
                data[key] = str_val
            except ValueError:
                module.fail_json(
                    msg='Error converting {} to string value'.format(value))

    try:
        cm = api.read_namespaced_config_map(name, namespace)
    except ApiException as e:
        if e.status == 404:
            create_config_map(api, name, namespace, data)
            module.exit_json(changed=True)
        else:
            module.fail_json(
                msg='Error attempting to read existing saved state: {}'.format(e))
    if should_update(cm.data, data):
        update_config_map(api, name, namespace, data)
        module.exit_json(changed=True)
    module.exit_json(changed=False)



def create_config_map(api, name, namespace, data):
    meta = client.V1ObjectMeta(name=name)
    body = client.V1ConfigMap(metadata=meta, data=data)
    try:
        res = api.create_namespaced_config_map(namespace, body)
    except ApiException as e:
        module.fail_json(
            msg='Error attempting to create required state management object: {}'.format(e))


def update_config_map(api, name, namespace, data):
    body = client.V1ConfigMap(data=data)
    try:
        res = api.patch_namespaced_config_map(name, namespace, body)
    except ApiException as e:
        module.fail_json(
            msg='Error attempting to update state: {}'.format(e))


def main():
    module = AnsibleModule(
        argument_spec = dict(
            fields=dict(required=True, type='dict')
        ),
    )
    if not HAS_K8_CLIENT:
        module.fail_json(
            msg='Error attempting to load kubernetes client: {}'.format(error))

    run(module)

if __name__ == '__main__':
    main()
