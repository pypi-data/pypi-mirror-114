from setuptools import setup, find_packages
import requests
import semantic_version

install_requires = [
    'boto3>=1.17.78',
    'botocore>=1.20.78'
]

def get_lucid_dynamodb_version():
    url = "https://pypi.org/pypi/LucidDynamodb/json"
    response = requests.request("GET", url, headers={}, data={})
    result = response.json()
    lucid_dynamodb_version = str(result.get("info").get("version"))
    current_version = semantic_version.Version(lucid_dynamodb_version)
    next_version = current_version.next_patch()
    return next_version

setup(
        name="LucidDynamodb",
        version=str(get_lucid_dynamodb_version()),
        author="Dinesh Sonachalam",
        author_email="dineshsonachalam@gmail.com",
        description="A simple Python wrapper to AWS Dynamodb",
        url="https://github.com/dineshsonachalam/Lucid-Dynamodb",
        long_description=open('README.md').read(),
        long_description_content_type='text/markdown',
        zip_safe=False,
        license='MIT',
        keywords='python dynamodb amazon',
        python_requires=">=3.1",
        install_requires=install_requires,
        packages=find_packages(),
        classifiers=[
                "Programming Language :: Python :: 3",
                "License :: OSI Approved :: MIT License",
                "Operating System :: OS Independent",
        ]
)