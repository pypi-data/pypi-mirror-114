import setuptools

setuptools.setup(
    name="extext",
    py_modules=['extext'],
    version="0.1",
    author="gd",
    description="Markup language.",
    long_description="Lightweight Markdown-like markup language",
    url="https://gitea.gch.icu/gd/extext/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: The Unlicense (Unlicense)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
