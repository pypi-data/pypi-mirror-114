from setuptools import setup, find_packages

setup_args = dict(
    name='epkeeperlib',
    version='1.0.0',
    author='Cheng Chen',
    author_email='tonychengchen@hotmail.com',
    description='EPKEEPER common utility package',
    long_description="",
    license='MIT',
    packages=find_packages(),
    url='https://gitee.com/tonychengchen/epkeeper_lib',
)

install_requires = [
    "pandas~=1.1.3",
    "PyMySQL~=0.9.3"
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)
