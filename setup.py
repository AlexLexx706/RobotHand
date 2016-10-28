from setuptools import setup, find_packages

setup(
    name='robothand',
    version='0.1',
    author='alexlexx',
    author_email='alexlexx1@gmail.com',
    packages=find_packages(),
    license='GPL',
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'configurator = robothand.configurator.widget:main'
        ],
    },
    package_data={
        'allarm_server.admin': [
            'configurator/*.ui',
            'servos_settings/*.ui']
    },
)
