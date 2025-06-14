#!/usr/bin/env python3

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import Command, FindExecutable, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    # Declare launch arguments
    declared_arguments = [
        DeclareLaunchArgument(
            'start_rviz', default_value='false', description='Whether to execute rviz2'
        ),
        DeclareLaunchArgument(
            'prefix',
            default_value='""',
            description='Prefix of the joint and link names',
        ),
        DeclareLaunchArgument(
            'use_sim',
            default_value='false',
            description='Start robot in Gazebo simulation.',
        ),
        DeclareLaunchArgument(
            'use_fake_hardware',
            default_value='false',
            description='Use fake hardware mirroring command.',
        ),
        DeclareLaunchArgument(
            'fake_sensor_commands',
            default_value='false',
            description='Enable fake sensor commands.',
        ),
        DeclareLaunchArgument(
            'port_name',
            default_value='/dev/ttyUSB0',
            description='Port name for hardware connection.',
        ),
    ]

    # Launch configurations
    start_rviz = LaunchConfiguration('start_rviz')
    prefix = LaunchConfiguration('prefix')
    use_sim = LaunchConfiguration('use_sim')
    use_fake_hardware = LaunchConfiguration('use_fake_hardware')
    fake_sensor_commands = LaunchConfiguration('fake_sensor_commands')
    port_name = LaunchConfiguration('port_name')

    # Generate URDF file using xacro
    urdf_file = Command([
        PathJoinSubstitution([FindExecutable(name='xacro')]),
        ' ',
        PathJoinSubstitution([
            FindPackageShare('open_manipulator_description'),
            'urdf',
            'om_x',
            'open_manipulator_x.urdf.xacro',
        ]),
        ' ',
        'prefix:=', prefix,
        ' ',
        'use_sim:=', use_sim,
        ' ',
        'use_fake_hardware:=', use_fake_hardware,
        ' ',
        'fake_sensor_commands:=', fake_sensor_commands,
        ' ',
        'port_name:=', port_name,
    ])
    robot_description = {'robot_description': urdf_file}

    # Path for controller YAML
    controller_manager_config = PathJoinSubstitution([
        FindPackageShare('open_manipulator_bringup'),
        'config',
        'om_x',
        'hardware_controller_manager.yaml',
    ])

    # Path for RViz config (optional)
    rviz_config_file = PathJoinSubstitution([
        FindPackageShare('open_manipulator_description'),
        'rviz',
        'open_manipulator.rviz',
    ])

    # Nodes
    control_node = Node(
        package='controller_manager',
        executable='ros2_control_node',
        parameters=[robot_description, controller_manager_config],
        output='both',
    )

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[robot_description, {'use_sim_time': use_sim}],
        output='screen',
    )

    # Spawner: Only joint_state_broadcaster and gravity_compensation_controller (¡MODIFICADO!)
    joint_state_broadcaster_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['joint_state_broadcaster'],
        output='screen',
    )
    gravity_controller_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['gravity_compensation_controller'],
        output='screen',
    )

    # Si quieres mantener el effort_controller, puedes dejarlo aquí. Si NO, elimina este bloque.
    # effort_controller_spawner = Node(
    #     package='controller_manager',
    #     executable='spawner',
    #     arguments=['effort_controller'],
    #     output='screen',
    # )

    # RViz (optional)
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', rviz_config_file],
        output='screen',
        condition=IfCondition(start_rviz),
    )

    return LaunchDescription(
        declared_arguments + [
            control_node,
            robot_state_publisher_node,
            joint_state_broadcaster_spawner,
            gravity_controller_spawner,
            # effort_controller_spawner, # Descomenta si lo necesitas
            rviz_node,
        ]
    )