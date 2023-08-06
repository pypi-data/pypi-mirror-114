import setuptools

setuptools.setup(
    name='ToGather',
    version='0.9.1',
    packages=setuptools.find_namespace_packages(include=['bin','bin.*']),
    package_data={'': ['bin/*']},
    include_package_data=True,
    install_requires=['PyQt5', 'qt_material', 'pyqtchart'],
    entry_points={
        'console_scripts': [
            'ToGather = bin.ToGatherRelease:main'
        ]
    },
    url='',
    license='',
    author='ToGather',
    author_email='',
    description=''
)
