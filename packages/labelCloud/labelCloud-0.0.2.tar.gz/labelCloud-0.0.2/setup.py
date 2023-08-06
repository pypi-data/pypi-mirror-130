from setuptools import setup

requirements = [
    "numpy~=1.21.2",
    "open3d~=0.13.0",
    "PyOpenGL~=3.1.5",
    "PyQt5~=5.15.4",
]

setup(
    name="labelCloud",
    version="0.0.2",
    description="A lightweight tool for labeling 3D bounding boxes in point clouds.",
    author="Christoph Sager",
    author_email="christoph.sager@gmail.com",
    url="https://github.com/ch-sa/labelCloud",
    packages=[
        "labelcloud",
        "labelcloud.ressources",
        "labelcloud.ressources.icons",
        "labelcloud.tests",
        "labelcloud.src.control",
        "labelcloud.src.label_formats",
        "labelcloud.src.labeling_strategies",
        "labelcloud.src.model",
        "labelcloud.src.utils",
        "labelcloud.src.view",
    ],
    package_data={"labelcloud.ressources": ["*"], "labelcloud.ressources.icons": ["*"]},
    entry_points={"console_scripts": ["labelcloud=labelcloud.__main__:main"]},
    install_requires=requirements,
    zip_safe=False,
    keywords="labelCloud",
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
