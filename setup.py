# Automatically created by: shub deploy

from setuptools import find_packages, setup

setup(
    name="project",
    packages=find_packages(),
    entry_points={"scrapy": ["settings = scrapy_project.settings"]},
    scripts=[
        "scripts/populate_redis_queue.py",
    ],
)
