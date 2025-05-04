"""Setup script for the georgian_guide package."""

from setuptools import find_packages, setup

if __name__ == "__main__":
    setup(
        name="georgian_guide",
        version="0.1.0",
        packages=find_packages(where="src"),
        package_dir={"": "src"},
        include_package_data=True,
        install_requires=[
            "pydantic>=2.5.0",
            "openai>=1.5.0",
            "fastapi>=0.103.1",
            "uvicorn>=0.23.2",
            "python-dotenv>=1.0.0",
        ],
        entry_points={
            "console_scripts": [
                "georgian-guide=georgian_guide.cli:main",
            ],
        },
    ) 