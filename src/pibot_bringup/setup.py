from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'omar_project'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # (os.path.join('share', package_name, 'omar_project'), ['omar_project/hallway_map.json']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
        (os.path.join('share', package_name, 'urdf'), glob('urdf/*')),
        (os.path.join('share', package_name, 'map'), glob('map/*')),
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
        (os.path.join('share', package_name, 'resource'), glob(os.path.join('resource', '*'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='omar elalaily',
    maintainer_email='omar.elalaily94@gmail.com',
    description='omar project packages',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'obstacle_avoid = autonomous_indoor.obstacle_avoid:main',
            'navigation_controller = autonomous_indoor.navigation_controller:main',
            'nav2_test = autonomous_indoor.nav2_test:main',
        ],
    },
)
