import setuptools

with open("README.md", "r", encoding="utf-8") as description:
    long_description = description.read()

setuptools.setup(
    name="pypi-package-guide",
    version="0.0.2",
    author="Mauricio Matias",
    author_email="xxx@xxx.io",
    description="This is a PYPI package template",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    url="https://github.com/cr0wg4n/pypi-package-guide",
    project_urls={
        "Bug Tracker": "https://github.com/cr0wg4n/pypi-package-guide/issues",
    },
    # more classifiers: https://pypi.org/classifiers/
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Operating System :: POSIX :: Linux',
        'License :: OSI Approved :: MIT License',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
    ],
    keywords=["template", "pypi-guide", "pypi"],
    packages=["pypi_package_guide"],
    package_data={
        'pypi_package_guide': [
            'data/*.txt',
        ]
    },
    # install_requires = ['requests', 'numpy'] etc...
    install_requires=[],
    python_requires=">=3.6",
)
