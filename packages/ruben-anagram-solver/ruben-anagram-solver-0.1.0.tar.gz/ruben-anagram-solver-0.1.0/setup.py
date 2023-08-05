import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ruben-anagram-solver",
    version="0.1.0",
    author="Ruben Dougall",
    author_email="info.ruebz999@gmail.com",
    description="Simple command-line anagram solver",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ruben9922/anagram-solver",
    keywords="anagram solver words strings command-line",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Natural Language :: English",
        "Topic :: Utilities",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': ['ruben-anagram-solver=anagram_solver:main'],
    },
    py_modules=['anagram_solver'],
)
