import json
import re
import time
import xml.etree.ElementTree as ET

import boto3
import os

with open("pom.xml") as f:
    xmlstring = f.read()

xmlstring = re.sub(r'\sxmlns="[^"]+"', '', xmlstring, count=1)
pom = ET.fromstring(xmlstring)
version = pom.find("version")

if "SNAPSHOT" in version.text:
    version_text = version.text + "-" + os.environ["CODEBUILD_BUILD_ID"]
else:
    version_text = version.text

with open("aws-fastup-build/launch_configs.config.json") as cr:
    launch_config_config = cr.read()

version_text = version_text.replace(".", "-").replace(":", "-")

launch_config_config = re.sub("REPLACEAPPTIERVERSIONNUMBERPARM", version_text, launch_config_config)

with open("aws-fastup-build/launch_configs.config.json", "w") as cw:
    cw.write(launch_config_config)

cf_client = boto3.client('cloudformation')
with open("aws-fastup-build/launch_configs.yaml") as template_stream:
    data = ""
    lines = template_stream.readlines()
    for line in lines:
        data += line
stack_name = "SpinSciCustomerApp-" + version_text
new_stack = cf_client.create_stack(
    StackName=stack_name,
    TemplateBody=data,
    Parameters=json.load(open("aws-fastup-build/launch_configs.config.json"))
)
stack_not_ready = True
timeout = 300
start_at = time.time()
while stack_not_ready:
    time.sleep(30)
    stack_status_dict = cf_client.describe_stacks(StackName=stack_name)
    print(stack_status_dict)
    if stack_status_dict["Stacks"][0]["StackStatus"] == "CREATE_COMPLETE":
        stack_not_ready = False
    if time.time() - start_at > timeout:
        raise Exception("Timeout waiting for stack " + stack_name + " to be created after " + str(timeout) + " seconds.")

with open("aws-fastup-build/asgs.staging.config.json") as cr:
    asg_config = cr.read()
    print(asg_config)

asg_config = re.sub("REPLACELAUNCHCONFIGSTACKNAME", stack_name, asg_config)
print(asg_config)
new_config = {"Parameters": {}}
for each_param in asg_config:
    new_config["Parameters"][each_param["ParameterKey"]] = each_param["ParameterValue"]

with open("aws-fastup-build/asgs.staging.config.json", "w") as cw:
    cw.write(new_config)

    # with open("aws-fastup-build/asgs.yaml") as template_stream:
    #     data = ""
    #     lines = template_stream.readlines()
    #     for line in lines:
    #         data += line
    # print data
    # new_stack = cf_client.update_stack(
    #     StackName="SpinSci-Asgs-1-0-0-staging",
    #     TemplateBody=data,
    #     Parameters=json.load(open("aws-fastup-build/asgs.staging.config.json"))
    # )
    # print(new_stack)
