from setuptools import setup, find_packages

setup(
    name="piuma",
    version="v1.0.0",
    license="gpl-3.0",
    author="Alessandro De Leo",
    author_email="emit07@protonmail.com",
    description="An ultra-lighweight document oriented database",
    packages=find_packages(),
    keywords=['python', 'database', 'document oriented'],
    url="https://github.com/emit07/piuma",
    python_requires='>=3.6'
)