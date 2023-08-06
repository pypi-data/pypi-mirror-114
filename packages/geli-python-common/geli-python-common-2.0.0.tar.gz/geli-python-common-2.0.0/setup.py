from setuptools import setup, find_packages


if __name__ == "__main__":

    __version__ = "2.0.0"

    # Get the requirements
    with open("requirements.txt", "r") as f:
        reqs = f.read().split('\n')

    setup(
        name="geli-python-common",
        author="Insung",
        author_email="insung.seok@qcells.com",
        description="Python common libraries package",
        install_requires=reqs,
        version=__version__,
        package_dir={"" : "src"},
        packages=find_packages(where="src",exclude = ['tests', '*.tests', '*.tests.*']), #TODO not excluding tests. Investigate the cause
        zip_safe=False,
        include_package_data=True,
    )