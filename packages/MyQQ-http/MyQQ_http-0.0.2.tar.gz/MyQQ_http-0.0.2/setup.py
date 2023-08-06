import setuptools
 
with open("README.md", "r") as fh:
    long_description = fh.read()
 
setuptools.setup(name="MyQQ_http",
                 version="0.0.2",
                 author="Marztop",
                 author_email="1332346968@qq.com", 
                 description="MyQQ_SDK python version",
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 url="https://github.com/marztop",
                 packages=setuptools.find_packages(),
                 classifiers=[
                     "Programming Language :: Python :: 3",
                     "License :: OSI Approved :: MIT License",
                     "Operating System :: OS Independent",
                 ],
                 python_requires='>=3.5',
                 py_modules=['MyQQ_http'],
                 install_requires=[
                     'requests>=0.1'
                 ]
)