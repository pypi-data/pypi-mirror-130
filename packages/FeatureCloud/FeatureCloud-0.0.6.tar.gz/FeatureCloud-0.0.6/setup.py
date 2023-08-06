import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(name="FeatureCloud",
                 version="0.0.6",
                 author="FeatureCloud",
                 author_email="mohammad.bakhtiari@uni-hamburg.de",
                 description="Secure Federated Learning Platform",
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 url="https://github.com/FeatureCloud/app-template",
                 project_urls={
                     "Bug Tracker": "https://github.com/FeatureCloud/app-template/issues",
                 },
                 classifiers=[
                     "Programming Language :: Python :: 3",
                     "Operating System :: OS Independent",
                 ],
                 packages=['FeatureCloud.apps', 'FeatureCloud.engine', 'FeatureCloud.api'],
                 python_requires=">=3.7",
                 entry_points={'console_scripts': ['FeatureCloud = FeatureCloud.__main__:fc_command',
                                                   ]
                               },

                 )
