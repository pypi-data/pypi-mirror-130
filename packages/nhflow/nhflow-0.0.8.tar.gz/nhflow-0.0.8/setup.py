#
# import setuptools
#
# setuptools.setup(
#     name="nhflow",
#     version="0.0.7",
#     author="@zjvis",
#     author_email="wzl@zhejianglab.com",
#     description="Serve contributors of the Nebula Hub to generate model configurations",
#     #url="https://github.com/pypa/sampleproject",
#     packages=setuptools.find_packages(),
#     classifiers=[
#         "Programming Language :: Python :: 3",
#         "License :: OSI Approved :: MIT License",
#         "Operating System :: OS Independent",
#     ],
#     python_requires='>=3.6',
#
#     # 安装过程中，需要安装的静态文件，如配置文件、service文件、图片等
#     data_files=[
#         # ('', ['conf/*.conf']),
#         # ('/usr/lib/systemd/system/', ['bin/*.service']),
#     ],
#
#     # 希望被打包的文件
#     package_data={
#         '': ['*.py'],
#         'bandwidth_reporter': ['*.py']
#     },
#     # 不打包某些文件
#     exclude_package_data={
#         'bandwidth_reporter': ['*.txt']
#     }
# )
#
# requires = [
#     "setuptools>=42",
#     "wheel"
# ]
#

import setuptools

# with open("README.md", "r", encoding="utf-8") as fh:
#     long_description = fh.read()

setuptools.setup(
    name="nhflow",
    version="0.0.8",
    author="Example Author",
    author_email="author@example.com",
    description="A small example package",
    # long_description=long_description,
    # long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    project_urls={
        "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
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