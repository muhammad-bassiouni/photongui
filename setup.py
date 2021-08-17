import pathlib
from setuptools import setup


CURRENT = pathlib.Path(__file__).parent


README = (CURRENT / "README.md").read_text()



install_requires = [
    'pyobjc-core ; sys_platform == "darwin"',
    'pyobjc-framework-Cocoa ; sys_platform == "darwin"',
    'pyobjc-framework-WebKit ; sys_platform == "darwin"',
]

extra_require = {
    'cef': ['cefpython3'],
}

setup(
    name="photongui",
    version="1.0.1",
    author="Muhammed Bassiouni",
    author_email="",
    description="Build GUI in Python with JavaScript, HTML, and CSS.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Mohamed501258/photongui",
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
    package_dir={'photongui': 'photongui'},
    packages=['photongui', 'photongui.api'],
    package_data={'photongui': ['photongui/gui/images/icon.png']},
    install_requires=install_requires,
    extra_requir=extra_require
)