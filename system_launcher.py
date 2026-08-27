#!/usr/bin/env python3
"""Project-wide process launcher for the four-PC harvest system.

This launcher starts only processes that belong to the selected local PC.  The
four PCs still share ROS 2 through the configured domain/network; this file does
not pretend to launch processes on another host.
"""

import argparse
import os
import signal
import subprocess
import sys
import time
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent
DEFAULT_ISAAC_PYTHON = Path("/home/rokey/isaacsim/python.sh")


def build_commands(args):
    python = Path(args.python)
    commands = []
    if args.role in ("gpu_pc1", "all-local"):
        isaac_python = Path(args.isaac_python)
        commands.append(
            (
                "isaac_sim",
                [
                    str(isaac_python),
                    str(PROJECT_DIR / "vision_apple_pick.py"),
                    "--robot-id",
                    args.robot_id,
                ],
            )
        )
        commands.append(
            (
                "harvest_coordinator",
                [
                    str(python),
                    str(PROJECT_DIR / "harvest_coordinator.py"),
                    "--robot-id",
                    "all",
                    "--execute",
                ],
            )
        )
    if args.role in ("personal_pc1", "all-local"):
        commands.append(
            (
                "apple_detector",
                [
                    str(python),
                    str(PROJECT_DIR / "base_apple_detector.py"),
                    "--robot-id",
                    "all",
                ],
            )
        )
    if args.role in ("personal_pc2", "all-local"):
        commands.append(
            (
                "quality_monitor",
                [
                    "ros2",
                    "launch",
                    "appleproj_personal_pc2",
                    "personal_pc2.launch.py",
                ],
            )
        )
    return commands


def parse_args():
    parser = argparse.ArgumentParser(description="Apple harvest system launcher")
    parser.add_argument(
        "--role",
        choices=("gpu_pc1", "personal_pc1", "personal_pc2", "all-local"),
        required=True,
        help="실행할 현재 PC 역할",
    )
    parser.add_argument(
        "--robot-id",
        choices=("robot_01", "robot_02"),
        default="robot_01",
        help="현재 Isaac Sim runtime에 연결할 robot profile",
    )
    parser.add_argument(
        "--isaac-python",
        default=str(DEFAULT_ISAAC_PYTHON),
        help="Isaac Sim 5.1.0 python.sh 경로",
    )
    parser.add_argument(
        "--python",
        default=sys.executable,
        help="ROS 2 Python 실행기 (기본: 현재 Python)",
    )
    parser.add_argument(
        "--startup-delay",
        type=float,
        default=2.0,
        help="Isaac Sim 시작 후 Coordinator를 시작하기 전 대기 시간",
    )
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def terminate_processes(processes):
    for process in processes:
        if process.poll() is None:
            process.send_signal(signal.SIGINT)
    deadline = time.monotonic() + 5.0
    while time.monotonic() < deadline and any(p.poll() is None for p in processes):
        time.sleep(0.1)
    for process in processes:
        if process.poll() is None:
            process.terminate()


def main():
    args = parse_args()
    commands = build_commands(args)
    for name, command in commands:
        print(f"[{name}] {' '.join(command)}")
    if args.dry_run:
        return 0

    processes = []
    try:
        for index, (name, command) in enumerate(commands):
            if index and name == "harvest_coordinator":
                time.sleep(max(0.0, args.startup_delay))
            environment = os.environ.copy()
            environment.setdefault("ROS_DOMAIN_ID", "102")
            process = subprocess.Popen(command, cwd=PROJECT_DIR, env=environment)
            processes.append(process)
            print(f"[{name}] started pid={process.pid}")
        while processes:
            if any(process.poll() is not None for process in processes):
                return_code = next(
                    process.returncode for process in processes if process.poll() is not None
                )
                return int(return_code or 0)
            time.sleep(0.5)
    except KeyboardInterrupt:
        return 130
    finally:
        terminate_processes(processes)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
