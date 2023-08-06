import setuptools
import versioneer

with open("README.rst", "r") as fhandle:
    long_description = fhandle.read()
with open("requirements.txt", "r") as fhandle:
    requirements = [line.strip() for line in fhandle]

setuptools.setup(
        name="is-num",
        version=versioneer.get_version(),
        cmdclass=versioneer.get_cmdclass(),
        author="Mark Yang",
        author_email="mark.xc.yang@gmail.com",
        description="A Python library to determine if something is a num.",
        long_description=long_description,
        long_description_content_type="text/x-rst",
        packages=setuptools.find_packages(),
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            ],
        python_requires='>=3.7',
        install_requires=requirements,
        )

        
