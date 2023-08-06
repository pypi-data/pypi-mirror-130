import setuptools

with open("readme.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
dirParent = "prediction"

setuptools.setup(
name="predictionconsoandrea", # Replace with your own username
version="1.0.0",
author="andrea massa",
author_email="massaaurore@yhaoo.com",
description="Utilities package",
long_description=long_description,
long_description_content_type="text/markdown",
# url="https://github.com/pypa/sampleproject",
# project_urls={
#     "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
# },
classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
],
# package_dir={"": dirParent},
# packages=['dorianUtils'],
packages=setuptools.find_packages(),
package_data={'': ['data/*']},
include_package_data=True,
install_requires=['IPython','pandas==1.3.1',
                'dash==1.20.0',
                'sklearn==0.0',
                'pandas==1.3.1',
                'matplotlib==3.4.2',
                'screeningBuilding==3.4.2',
                'seaborn==0.11.2',
                'yellowbrick==1.3.post1'
],
python_requires=">=3.8"
)
