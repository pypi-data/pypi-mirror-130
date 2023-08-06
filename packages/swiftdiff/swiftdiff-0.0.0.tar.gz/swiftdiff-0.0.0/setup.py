import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="swiftdiff",
    author="Nadine Lee, Li Sun, Alice Cai",
    author_email="nadine_lee@college.harvard.edu, lsun@g.harvard.edu, acai@college.harvard.edu",
    description="SwiftDiff performs automatic differentiation (AD) for the user.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cs107-swiftdiff/cs107-FinalProject",
    project_urls={
        "Bug Tracker": "https://github.com/cs107-swiftdiff/cs107-FinalProject/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)