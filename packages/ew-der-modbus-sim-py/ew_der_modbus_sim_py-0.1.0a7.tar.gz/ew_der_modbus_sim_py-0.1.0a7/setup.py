from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

install_requires = [
    "modbus-tk==1.1.2",
    "pysunspec2==1.0.4",
    "python-dotenv==0.1"
]

tests_requires = [
    "pytest==6.2.2",
    "pytest-cov==2.11.1"
]

dev_requires = [
    "twine==3.4.1",
    "build==0.3.1"
]

setup(
    name="ew_der_modbus_sim_py",
    version="0.1.0a7",
    author="Pablo Buitrago",
    author_email="messaging@energyweb.org",
    description="EnergyWeb DER Modbus Simulator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/energywebfoundation/ew_der_modbus_sim_py.git",
    project_urls={
        "Bug Tracker": "https://github.com/energywebfoundation/ew_der_modbus_sim_py/issues",
    },
    license='LICENSE',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
    ],
    keywords="decentralised iot der modbus sunspec flexibility",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.7",
    install_requires=install_requires,
    tests_require=install_requires + tests_requires,
    extras_require={
        "all": install_requires + tests_requires + dev_requires,
        "test": install_requires + tests_requires
    }
)