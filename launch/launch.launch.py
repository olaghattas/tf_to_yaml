from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():
    ld = LaunchDescription()

    aptags_tf = Node(
        package="tf_to_yaml",
        executable="get_yaml_aptags",
        name="aptags_tf",
    )

    ld.add_action(aptags_tf)

    rooms_tf = Node(
        package="tf_to_yaml",
        executable="get_yaml_rooms",
        name="rooms_tf"
    )

    ld.add_action(rooms_tf)

    return ld
