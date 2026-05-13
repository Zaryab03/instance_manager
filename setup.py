from setuptools import find_packages, setup


setup(
    name="instance_manager",
    version="1.0.0",
    description="Manage instance limits, user counts, and license expiry for Frappe",
    packages=find_packages(include=["instance_manager", "instance_manager.*"]),
    include_package_data=True,
)
