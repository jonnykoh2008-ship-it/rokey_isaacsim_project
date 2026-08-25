from glob import glob
from setuptools import find_packages, setup


package_name = "appleproj_personal_pc2"


setup(
    name=package_name,
    version="0.0.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", [f"resource/{package_name}"]),
        (f"share/{package_name}", ["package.xml"]),
        (f"share/{package_name}/launch", glob("launch/*.launch.py")),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="TBD",
    maintainer_email="tbd@example.com",
    description="Monitoring and inspection retry tools for Personal PC 2.",
    license="TBD",
    entry_points={
        "console_scripts": [
            "quality_monitor = appleproj_personal_pc2.quality_monitor:main",
            "retry_inspection = appleproj_personal_pc2.retry_inspection:main",
        ],
    },
)
