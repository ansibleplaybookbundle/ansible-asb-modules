#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule

ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: asb_save_test_result
short_description: Encodes the test results for testing action.
description:
     - Takes a test result object and makes it available during the testing
     action.
notes: []
requirements: []
author:
    - "Red Hat, Inc."
options:
  fail:
    description:
      - 'Will signify whether the test result has passed or failed.'
    default: false
    type: bool
  msg:
    description:
      - 'The message that will be printed with the failure or success'
    type: string
'''

EXAMPLES = '''
- name: save test results
  asb_save_test_result:
    fail: true
    msg: "Test failed"

- name: test passed
  asb_save_test_result:
    msg: "Test passed!"
'''
RETURN = '''
'''

TEST_RESULT_PATH = "/var/tmp/test-result"


def main():
    """Ansible module that will Append test result to test result file."""
    argument_spec = dict(
        fail=dict(default=False, type='bool'),
        msg=dict(default=None, type='str')
    )

    ansible_module = AnsibleModule(argument_spec=argument_spec)
    try:
        with open(TEST_RESULT_PATH, "a") as test_result_file:
            # If failure is true then print the 1 code the test file.
            if ansible_module.params['fail']:
                test_result_file.write("1\n")
            else:
                # If failue is false, then 0 code signals success.
                test_result_file.write("0\n")

            if ansible_module.params['msg'] is not None:
                test_result_file.write("%s\n" % ansible_module.params['msg'])
    except Exception as error:
        ansible_module.fail_json(msg="Error attempting to write test result: {}".format(error))

    ansible_module.exit_json(changed=True)


if __name__ == '__main__':
    main()
