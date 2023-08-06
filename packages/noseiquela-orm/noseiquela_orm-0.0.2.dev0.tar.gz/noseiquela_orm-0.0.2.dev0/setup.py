from setuptools import setup

# Metadata goes in setup.cfg. These are here for GitHub's dependency graph.
setup(
    name="noseiquela_orm",
    version="0.0.2-dev",
    install_requires=[
        "python-dateutil~=2.8",
        "google-cloud-datastore~=2.3",
        "google-api-core~=2.1",
        "google-auth~=2.3",
        "google-cloud-core~=2.1",
        "googleapis-common-protos~=1.53"
    ]
)
