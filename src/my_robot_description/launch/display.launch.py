from launch import LaunchDescription
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.actions import Node
from launch.substitutions import Command
import os
from ament_index_python.packages import get_package_share_path, get_package_share_directory

def generate_launch_description():
    
    urdf_file_name = 'my_robot.urdf.xml'

    urdf = os.path.join(
        get_package_share_path('my_robot_description'), 'urdf',
        urdf_file_name)
    
    print("urdf path ", urdf)

    with open(urdf, 'r') as infp:
        robot_desc = infp.read()

    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{'robot_description': robot_desc}]
    )

    joint_state_publisher_gui_node = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui"
    )

    rviz_config_path = os.path.join(get_package_share_path('my_robot_description'),
                                    'rviz', 'mb_urdf_convig.rviz')
    

    print('rviz config path ', rviz_config_path)


    rviz2_node = Node(
        package="rviz2",
        executable="rviz2",
        arguments=['-d', rviz_config_path]
    )

    return LaunchDescription([
        robot_state_publisher_node,
        joint_state_publisher_gui_node,
        rviz2_node
    ])