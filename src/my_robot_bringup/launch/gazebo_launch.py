import os

from ament_index_python.packages import get_package_share_directory, get_package_share_path

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node


def generate_launch_description():
    # Import the model urdf (load from file, xacro ...)
    urdf_file_name = 'my_robot.urdf.xml'

    urdf = os.path.join(
        get_package_share_path('my_robot_description'), 'urdf',
        urdf_file_name)
    
    print("urdf path ", urdf)

    with open(urdf, 'r') as infp:
        robot_desc = infp.read()

    # Robot state publisher
    params = {'use_sim_time': True, 'robot_description': robot_desc}
    robot_state_publisher = Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[params],
            arguments=[])

    # Gazebo Sim
    pkg_ros_gz_sim = get_package_share_directory('ros_gz_sim')
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_ros_gz_sim, 'launch', 'gz_sim.launch.py')),
        launch_arguments={'gz_args': '-r empty.sdf'}.items(),
    )


    joint_state_publisher_gui_node = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui"
    )


    # RViz
    pkg_my_robot_bringup = get_package_share_directory('my_robot_description')
    rviz = Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', os.path.join(pkg_my_robot_bringup, 'rviz', 'mb_urdf_convig.rviz')])

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
        joint_state_publisher_gui_node,
        rviz,
        spawn
    ])