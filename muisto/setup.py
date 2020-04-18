from setuptools import setup

setup(
    name="Muisto",
    version="1.0.0",
    install_requires=["requests","beautifulsoup4"],
    entry_points={
        "console_scripts": [
            "muisto = app:main"
        ]
    }
)
