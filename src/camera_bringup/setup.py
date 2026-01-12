from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'inventory_verification'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='rosdev',
    maintainer_email='omar.elalaily94@gmail.com',
    description='Detect ArUco IDs',
    license='TODO: License declaration',
    extras_require={
        'test': ['pytest'],
    },
    entry_points={
        'console_scripts': [
            'detect_aruco = inventory_verification.detect_aruco:main',
            'aruco_logger = inventory_verification.aruco_logger:main',
        ],
    },
)
