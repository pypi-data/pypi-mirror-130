import setuptools
setuptools.setup(

    name='zcts',
    version='0.0.6',
    description="ZD Converter 2000 python SDK",
    long_description="ControlZD Converter 2000  via python SDK, send serial commands via COM connection.",
    # long_description_content_type='text/markdown',
    author='zhengkunli',
    author_email="1st.melchior@gmail.com",
    python_requires= '>=3.8.0',
    url='https://github.com/Klareliebe7/zcts',
    packages=setuptools.find_packages(),
    # entry_points={
    #     'console_scripts': ['mycli=mymodule:cli'],
    # },
    install_requires= ["pyserial","colorama"],
    license='MIT',
    classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    ]

)