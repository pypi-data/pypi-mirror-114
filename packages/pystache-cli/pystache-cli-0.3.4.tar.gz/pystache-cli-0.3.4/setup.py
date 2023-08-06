from setuptools import setup

if __name__ == "__main__":

    with open("README.md", encoding="utf-8") as file:
        long_description = file.read()

    setup(
        packages=['pystache_cli'],
        keywords=["cli", "pystache", "template"],
        install_requires=["pystache"],        
        name='pystache-cli',
        description="Extended command line client for pystache",
        long_description=long_description,
        long_description_content_type="text/markdown",  # text/markdown or text/x-rst or text/plain
        version="0.3.4",
        author="Christian Winger",
        author_email="c@wingechr.de",
        url="https://github.com/wingechr/pystache-cli",
        download_url="https://github.com/wingechr/pystache-cli",
        platforms=["any"],
        license="Public Domain",
        project_urls={"Bug Tracker": "https://github.com/wingechr/pystache-cli",},
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication",
            "Operating System :: OS Independent",
        ],
        entry_points={
            "console_scripts": ["pystache-cli = pystache_cli.pystache_cli:main"]
        },
        package_data={"tests": ["data/**"]},
    )
