from setuptools import setup

setup(
    name='gcloud-dyndns',
    version='1.0.1',
    packages=['gcloud_dynamic_dns'],
    scripts=['bin/update-gcloud-dns'],
    url='https://github.com/jasonrig/gcloud-dyndns',
    license='MIT',
    author='Jason Rigby',
    author_email='hello@jasonrig.by',
    description='Update GCP Cloud DNS using the host\'s publicly visible IP address',
    install_requires=[
        'google-cloud-dns>=0.33.0,<0.34',
        'requests>=2.25.0,<2.26'
    ]
)
