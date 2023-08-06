from setuptools import setup, find_packages
setup(
    name = "diran",
    version = "1.1",
    py_modules = ['diran'],
    author = "Dmeng",
    author_email = "ecodemo520@outlook.com",
    license="GPLv3",
    packages=find_packages(),
    description = "搜索并分析你的文件夹",
    install_requires = [
        'prettytable>=2.1.0',
    ],
    include_package_data=True,
    zip_safe = True,
    entry_points={
        'console_scripts': [
            'diran = diran.__main__:main'
        ]
    },
    python_requires = '>=3'
)

