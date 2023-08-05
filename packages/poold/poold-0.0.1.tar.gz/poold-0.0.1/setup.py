from setuptools import find_packages, setup

setup(
    name="poold",
    version="0.0.1",
    author="Genevieve Flaspohler and Lester Mackey",
    author_email="geflaspohler@gmail.com",
    description="Python library for Optimistic Online Learning under Delay",
    url="https://github.com/geflaspohler/poold",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    package_dir={"": "poold"},
    packages=find_packages(where="poold"),
    install_requires=['pandas',
                      'numpy',                     
                      'matplotlib',                     
                      'seaborn',                     
                      'scipy',                     
                      ],
    python_requires=">=3.6",
)
