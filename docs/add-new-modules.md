# Adding New Modules

This document will cover the basics of creating a new APB module and testing the module.


## Writing the module

Modules go under the `library` folder and should be named after the module they provide. For example the module for providing a last_operation update is named: ```asb_last_operation.py```

The module should be well documented with clear examples provided.

Before writing a new module, it is recommended to create an issue on this repo outlining the functionality that you would like to see the module provide. This will promote discussion and a sharing of ideas to come up with the correct solution before any code has been written.

## Testing the module

The APB modules are intended to run from within the context of a Docker image as part of a POD running in a Kubernetes or OpenShift environment. They regularly will need to interact with resources created within these environments. In order to test your module you will need to take the following steps.

1) Create or reuse an existing APB

2) Modify your Docker image to add your python module file to the following location:
``` /etc/ansible/roles/ansibleplaybookbundle.asb-modules/library/ ```

Example:

``` 
COPY asb_last_operation.py /etc/ansible/roles/ansibleplaybookbundle.asb-modules/library/ 
```

3) In your APB playbooks add calls to your new module.

4) Build a new image and push it to your docker org

```
docker build -t <org>/my-apb:<TAG> .
docker push <org>/my-apb:<TAG>

```

5) Ensure your Ansible Broker is configured to look for APBs in the docker org where you have pushed the test APB
You can edit the config on a local OpenShift using the commands below:
```
oc login -u system:admin
oc project ansible-service-broker
oc edit configmap broker-config
```

You will find the org key under the registry section.

6) Perform the action that will call the playbook where your module is called from (provision,bind,update,deprovision, unbind)

## Debugging 

To debug the module, you can login to your cluster as a cluster admin then view the logs of the APB pod that is created, if there is a problem with your module, these logs should give you insight into what is happening.

The following commands will help:
```
oc login -u system:admin #if on local OpenShift cluster

oc get projects

oc get pods dh-<serviceName>-apb-prov-<RANDOM_STRING>

oc logs apb-<GENERATED_HASH> -n dh-<serviceName>-apb-prov-<RANDOM_STRING>
```

Notice the project name has apb-prov in its name this means it is an APB pod running the provision playbook.