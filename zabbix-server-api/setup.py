from setuptools import setup, find_packages

setup(
    name="zabbix-sdk",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "requests>=2.25.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0.0",
        ],
    },
    python_requires=">=3.7",
    author="Your Name",
    author_email="your.email@example.com",
    description="A Python SDK for the Zabbix API using MCP pattern",
    keywords="zabbix, api, sdk",
    url="https://github.com/yourusername/zabbix-sdk",
)
