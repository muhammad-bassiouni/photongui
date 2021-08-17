import pathlib
from setuptools import setup


HERE = pathlib.Path(__file__).parent


README = (HERE / "README.md").read_text()


setup(
    name="photongui",
    version="1.0.1",
    description="Build GUI in Python with JavaScript, HTML, and CSS.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Mohamed501258/photongui",
    author="Muhammed Bassiouni",
    author_email="",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        'Operating System :: OS Independent',
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    include_package_data=True,
    packages=['photongui', 'photongui.api'],
    package_data={'photongui': ['photongui/gui/images/icon.png']},
    install_requires=["cefpython3", "AppKit", "pyobjc"],
)