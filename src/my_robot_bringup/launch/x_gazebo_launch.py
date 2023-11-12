# Copyright 2019 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

from ament_index_python.packages import get_package_share_directory, get_package_share_path

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node


def generate_launch_description():

    
    urdf_file_name = 'my_robot.urdf.xml'

    urdf = os.path.join(
        get_package_share_path('my_robot_description'), 'urdf',
        urdf_file_name)
    
    print("urdf path ", urdf)

    with open(urdf, 'r') as infp:
        robot_desc = infp.read()

    # Robot state publisher
    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{'robot_description': robot_desc}]
    )
    rviz_config_path = os.path.join(get_package_share_path('my_robot_bringup'),
                                    'rviz', 'mb_urdf_convig.rviz')
    rviz = Node(
        package="rviz2",
        executable="rviz2",
        arguments=['-d', rviz_config_path]
    )

    # Robot state publisher
    # params = {'use_sim_time': True, 'robot_description': robot_desc}
    # robot_state_publisher = Node(
    #         package='robot_state_publisher',
    #         executable='robot_state_publisher',
    #         name='robot_state_publisher',
    #         output='screen',
    #         parameters=[params],
    #         arguments=[])

    # Gazebo Sim
    pkg_ros_gz_sim = get_package_share_directory('ros_gz_sim')
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_ros_gz_sim, 'launch', 'gz_sim.launch.py')),
        launch_arguments={'gz_args': '-r empty.sdf'}.items(),
    )

    # <node pkg="rviz2" exec="rviz2" output="screen" 
    #   args="-d $(var rviz_config_path)" />

    # RViz
    # pkg_ros_gz_sim_demos = get_package_share_directory('rviz')
    # rviz = Node(
    #     package='rviz2',
    #     executable='rviz2',
    #     arguments=[
    #         '-d',
    #         os.path.join(pkg_ros_gz_sim_demos, 'rviz', 'robot_description_publisher.rviz')
    #     ]
    # )
    # rviz_config_path = os.path.join(get_package_share_path('my_robot_bringup'), 'rviz', 'urdf_config.rviz')


    # Spawn
    spawn = Node(package='ros_gz_sim', executable='create',
                 arguments=[
                    '-name', 'my_custom_model',
                    '-x', '1.2',
                    '-z', '2.3',
                    '-Y', '3.4',
                    '-topic', '/robot_description'],
                 output='screen')

    return LaunchDescription([
        gazebo,
        robot_state_publisher,
        rviz,
        spawn
    ])