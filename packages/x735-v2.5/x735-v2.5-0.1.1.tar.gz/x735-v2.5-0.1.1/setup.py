import setuptools

setuptools.setup(
    name="x735-v2.5",
    version="0.1.1",
    description="Library for board x735",
    author="sh.kiruh@gmail.com",
    install_requires=[
        "pigpio==1.78",
        "RPi.GPIO==0.7.0",
        "click==8.0.1",
    ],
    extras_require={"dev": ["pre-commit"]},
    entry_points={
        "console_scripts": ["x735fan=main:fan"],
    },
)
