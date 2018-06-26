#!/usr/bin/python

DOCUMENTATION = '''
---
lookup: asb_state
short_description: Retrieve state previously set by the Ansible Service Broker
description:
     - Provides a secure method for allowing Service Bundle developers
       to access previously set state during a Service Bundle action.
author:
    - "Red Hat, Inc."
options:
    _terms:
        description:
            - Key(s) to fetch the state value for.
        required: False
    get_all:
        description: >
          Get values for all set state.
          Returns a list with single value which is a dictionary of key, values.
        type: bool
        required: False
        default: False
    env:
        # Set via ASB StateManager
        - name: BUNDLE_STATE_LOCATION
          value: /etc/apb/state
notes: >
  _terms as a list of keys and get_all are mutually exclusive.
  If key(s) are provided, they will take priority and
  their values will be returned as a list.
'''

EXAMPLES = '''
# Example with no keys provided and get_all arg set to True
- name: Get all state
  debug:
    msg: "The value for previously set state example=true is {{ lookup('asb_state', get_all=True).example }}"


# Example for fetching a single key
- name: Get state for single key
  debug:
    msg: "The value for key example is {{ lookup('asb_state', 'example') }}"


# Example get state for multiple keys
- name: test the new asb_state lookup plugin
  set_fact:
    some_test_var: "{{ lookup('asb_state', 'example_key', 'example_key_two') }}"


# Example to fetch state in loop
- debug:
    msg: 'Value is equal to {{item}}'
  with_asb_state:
    - 'example_key'
    - 'example_key_two'
'''

RETURN = """
  _raw:
    description:
      - The value(s) for set state
    type: list
"""

import os

from ansible.errors import AnsibleError, AnsibleFileNotFound, AnsibleParserError
from ansible.plugins.lookup import LookupBase

class LookupModule(LookupBase):

    def run(self, terms, variables=None, **kwargs):
        base_state_path = os.getenv('BUNDLE_STATE_LOCATION', '/etc/apb/state')
        ret = []

        if not terms and kwargs.get('get_all'):
            state_dict = {}
            keys = os.listdir(base_state_path)
            for key in keys:
                if os.path.isdir(os.path.join(base_state_path, key)):
                    continue
                conf_file = '{}/{}'.format(base_state_path, key)
                state_dict[key] = self.get_state(key, conf_file)
            ret.append(state_dict)
            return ret

        for term in terms:
            conf_file = '{}/{}'.format(base_state_path, term)
            ret.append(self.get_state(term, conf_file))
        return ret

    def get_state(self, key, conf_file):
        try:
            b_contents, show_data = self._loader._get_file_contents(conf_file)
        except AnsibleFileNotFound:
            raise AnsibleError('no state found for key {}'.format(key))
        except AnsibleParserError:
            raise AnsibleError('error reading state for key {}'.format(key))
        return b_contents.decode("utf-8").rstrip()

