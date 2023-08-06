from setuptools import setup, find_packages
import os
import re


def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except IOError:
        return "File '%s' not found.\n" % fname


def readVersion():
    txt = read("edgefarm_application/version.py")
    ver = re.findall(r"([0-9]+)", txt)
    print("ver=%s" % ver)
    return ver[0] + "." + ver[1] + "." + ver[2]


setup(
    name="edgefarm_application",
    install_requires=[
        "asyncio-nats-client~=0.11.4",
        "fastavro~=1.4.0",
        "azure-iot-device~=2.7.0",
    ],
    version=readVersion(),
    description="A python library for EdgeFarm applications",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/edgefarm/edgefarm-application-sdk.py",
    project_urls={
        "Source Code": "https://github.com/edgefarm/edgefarm-application-sdk.py.git",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    author="Ci4Rail GmbH",
    author_email="engineering@ci4rail.com",
    license_files="LICENSE",
    packages=find_packages(where="."),
    package_data={'edgefarm_application': ['ads_node_module/ads_data.avsc', 'alm_mqtt_module/*.avsc']},
    setup_requires=['wheel']
)
