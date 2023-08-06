# https://packaging.python.org/tutorials/packaging-projects/#creating-setup-py
# setup.py is the build script for setuptools.
# It tells setuptools about your package (such
# as the name and version) as well as which code files to include
import io
import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

# with open(os.path.join(os.path.dirname(__file__), 'README')) as readme:
#     long_description = readme.read()
# long_description = open('README').read(),

package_root = os.path.abspath(os.path.dirname(__file__))

readme_filename = os.path.join(package_root, "README")
with io.open(readme_filename, encoding="utf-8") as readme_file:
    long_description = readme_file.read()

requirements = [
    'requests>=2.20.0,<3.0',
    'python-dateutil'
]

setup(
    title="contentstack-python",
    name="Contentstack",
    status="Active",
    type="process",
    created="09 Jun 2020",
    keywords="contentstack-python",
    version="1.6.0",
    author="Contentstack",
    author_email="shailesh.mishra@contentstack.com",
    description="Contentstack is a headless CMS with an API-first approach.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/contentstack/contentstack-python",
    packages=['contentstack'],
    license='MIT',
    test_suite='tests',
    install_requires=requirements,
    include_package_data=True,
    universal=1,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.6',
    zip_safe=False,
)
