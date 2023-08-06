import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

requirements = ["lzstring", "requests", "pycryptodome"]

setuptools.setup(
	name="pythonbpjs",
	version="0.0.1",
	author="Moriz",
	author_email="morizbebenk@gmail.com",
	description="Aplikasi Python yang digunakan untuk menangani proses dekripsi respon data dari bridging BPJS VCLAIM REST 2.0 (Encrypted Version). Support VCLAIM v1 dan API JKN (Antrean RS).",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/morizbebenk/pythonbpjs",
    project_urls={
        "Bug Tracker": "https://github.com/morizbebenk/pythonbpjs/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)