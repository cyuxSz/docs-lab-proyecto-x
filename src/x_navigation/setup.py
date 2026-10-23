from glob import glob
from setuptools import setup

package_name = 'x_navigation'

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/config', glob('config/*.yaml')),
        ('share/' + package_name + '/missions', glob('missions/*.yaml')),
    ],
    install_requires=['setuptools'],
    entry_points={
        'console_scripts': [
            'waypoint_follower = x_navigation.waypoint_follower:main',
            'old_planner = x_navigation.old_planner:main',
        ],
    },
)
