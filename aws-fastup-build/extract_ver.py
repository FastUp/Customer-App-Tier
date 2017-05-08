import re
import xml.etree.ElementTree as ET
import sys

with open("pom.xml") as f:
    xmlstring = f.read()

xmlstring = re.sub(r'\sxmlns="[^"]+"', '', xmlstring, count=1)
pom = ET.fromstring(xmlstring)
version = pom.find("version")

if "SNAPSHOT" in version.text:
    version_text = version.text + os.environ("CODEBUILD_BUILD_ID")
else:
    version_text = version.text

with open("aws-fastup-build/launch_configs.config.json") as cr:
    launch_config_config = cr.read()

launch_config_config = re.sub("REPLACEAPPTIERVERSIONNUMBERPARM", version_text, launch_config_config)

with open("aws-fastup-build/launch_configs.config.json", "w") as cw:
    cw.write(launch_config_config)

sys.stdout.write(version_text)
sys.exit(0)

