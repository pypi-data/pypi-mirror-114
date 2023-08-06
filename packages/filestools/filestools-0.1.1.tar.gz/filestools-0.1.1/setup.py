"""
CSDN主页：https://blog.csdn.net/as604049322
"""

import setuptools

with open("README.md", "r", encoding="u8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="filestools",
    version="0.1.1",
    author="小小明",
    author_email="604049322@qq.com",
    description="仿Linux的tree命令、文件差异比较工具、图片加水印和curl请求转python代码。",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url="https://github.com/pypa/sampleproject",
    license="GPLv3",
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    package_data={'watermarker': ['font/*'], },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=[
        'rich >= 9.13.0',
        'Pillow',
        'cchardet',
        "pyperclip >= 1.8.0"
    ],
    platforms='any',
    zip_safe=True,
    entry_points={
        'console_scripts': ["tree = treedir.__main__:main",
                            "tree2 = treedir.__main__:main",
                            "diff = filediff.__main__:main",
                            "marker = watermarker.__main__:main",
                            "curl2py = curl2py.__main__:main"]},
    python_requires=">=3.6"
)
