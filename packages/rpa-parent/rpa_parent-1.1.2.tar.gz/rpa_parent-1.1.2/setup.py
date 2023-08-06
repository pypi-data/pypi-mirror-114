import setuptools
setuptools.setup(
    name="rpa_parent",
    version="1.1.2",
    author="phfund",
    author_email="xxx@phfund.com.cn",
    description="rpa_parent",
    url="http://gitlab.phfund.com.cn/rpa/rpa-base/rpa-parent.git",
    packages=setuptools.find_packages(),
    package_data={
        '':['dependlibs/sikulixapi.jar'],  # 任何包中含有jar的文件
    },
    install_requires=[
        'requests==2.23.0',
        'numpy==1.18.4',
        'psutil==5.7.3',
        'uiautomation==2.0.7',
        'opencv_python==4.2.0.34',
        'pywin32==300',
        'PyGetWindow==0.0.9',
        'cx_Oracle==8.1.0',
        'JPype1==1.2.1',
        'Pillow==8.1.0',
        'selenium==3.141.0',
        'xlrd==1.2.0'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)