from setuptools import setup, find_packages
import versioneer


setup(
    name="gosu",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "plumbum",
        "typer",
        "python-dotenv",
        "semver",
        "pytest",
        "pyupgrade",
        "isort",
        "black",
        "flake8",
        "mccabe",
        "flake8-comprehensions",
        "flake8-print",
        "flake8-cognitive-complexity",
    ],
    license_files=("LICENSE",),
    entry_points={"console_scripts": ("gosu = gosu.main:app",)},
)
