import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyfetchh",
    version="1.5.3",
    author="Kreato",
    author_email="gamzeli_kerim@outlook.com",
    description="Stylish and simple fetch for your terminal that is customizable, and fast.",
    install_requires=[
   'colorama',
   'distro',
   'psutil'
],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kreat0/pyfetch",
    project_urls={
        "Bug Tracker": "https://github.com/kreat0/pyfetch",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
    ],
    scripts=['pyfetch'],
    python_requires=">=3.5",
)
