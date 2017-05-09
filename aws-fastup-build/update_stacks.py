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
pom_artifact_id = pom.find("artifactId")
print(version.text)
print(pom_artifact_id.text)
war_file_name = pom_artifact_id.text + "-" + version.text + ".war"
print(war_file_name)
if "SNAPSHOT" in version.text:
    version_text = version.text + "-" + os.environ["CODEBUILD_BUILD_ID"]
else:
    version_text = version.text

s3 = boto3.client("s3")
war_file_key = "war_files/" + os.environ["CODEBUILD_BUILD_ID"].replace(":", "-") + "/" + war_file_name
release_bucket_name = "spinsci-entities-1-0-0-sta-releaseartifactsbucket-mtqcxm5k34ox"
upload_file_return = s3.upload_file("target/" + war_file_name, release_bucket_name, war_file_key)
print(upload_file_return)
# region_prefix = "" if os.environ["AWS_DEFAULT_REGION"] == "us-east-1" else "-" + os.environ["AWS_DEFAULT_REGION"]
# war_s3_url = "https://" + release_bucket_name + ".s3" + region_prefix + ".amazonaws.com/" + war_file_key
# print(war_s3_url)

with open("aws-fastup-build/launch_configs.config.json") as cr:
    launch_config_config = cr.read()

version_text = version_text.replace(".", "-").replace(":", "-")
# launch_config_config = re.sub("REPLACEAPPTIERVERSIONNUMBERPARM", version_text, launch_config_config)

launch_config_config = re.sub("REPLACE_RELEASEARTIFACTSBUCKETPARM", release_bucket_name, launch_config_config)
launch_config_config = re.sub("REPLACE_RELEASEWARFILEKEYPARM", war_file_key, launch_config_config)
launch_config_config = re.sub("REPLACE_WARFILENAME", war_file_name, launch_config_config)

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

asg_config = re.sub("REPLACE_LAUNCHCONFIGSTACKNAME", stack_name, asg_config)
asg_config = re.sub("REPLACE_CONTEXTROOTPARM", war_file_name.replace(".war",""), asg_config)
print(asg_config)
new_config = {"Parameters": {}}
for each_param in json.loads(asg_config):
    new_config["Parameters"][each_param["ParameterKey"]] = each_param["ParameterValue"]
print(new_config)
with open("aws-fastup-build/asgs.staging.config.json", "w") as cw:
    json.dump(new_config, cw)

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
