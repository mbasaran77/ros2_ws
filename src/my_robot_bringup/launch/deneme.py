import os

from ament_index_python.packages import get_package_share_directory, get_package_share_path



pkg_ros_gz_sim_demos = get_package_share_directory('my_robot_bringup')
print(pkg_ros_gz_sim_demos)

d = os.path.join(pkg_ros_gz_sim_demos, 'rviz', 'mb_urdf_convig.rviz')

print(d)