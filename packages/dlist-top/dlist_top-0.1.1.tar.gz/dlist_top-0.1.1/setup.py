from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='dlist_top',
    version='0.1.1',
    description='DList.top client for Python',
    long_description=readme,
    long_description_content_type="text/markdown",
    author='DList.top',
    # author_email='',
    url='https://github.com/dlist-top/client-py',
    license=license,
    packages=find_packages(where='dlist_top', exclude=('test')),
    package_dir={"": "dlist_top"},
    python_requires=">=3.8",
)
