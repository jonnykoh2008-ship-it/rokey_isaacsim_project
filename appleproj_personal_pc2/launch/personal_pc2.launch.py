"""Launch the Personal PC 2 quality and checkpoint monitor."""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "deadline_checkpoint_id",
                default_value="",
                description=(
                    "Checkpoint EXIT that represents camera ROI exit. "
                    "Leave empty while its repository requirement remains TBD."
                ),
            ),
            Node(
                package="appleproj_personal_pc2",
                executable="quality_monitor",
                name="quality_monitor",
                output="screen",
                parameters=[
                    {
                        "use_sim_time": True,
                        "deadline_checkpoint_id": LaunchConfiguration(
                            "deadline_checkpoint_id"
                        ),
                        "result_deadline_sec": 0.5,
                    }
                ],
            ),
        ]
    )
