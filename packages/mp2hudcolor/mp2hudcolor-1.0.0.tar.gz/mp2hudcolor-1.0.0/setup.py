from setuptools import setup, Extension, find_packages
from Cython.Distutils import build_ext

src = ['src/mp2hudcolor_wrapper.pyx']

extensions = [
    Extension("mp2hudcolor", src)
]

setup(
    name="mp2hudcolor",
    version="1.0.0",
    description="Modifies an existing NTWK file for Metroid Prime 2: Echoes and changing the color of the HUD.",
    long_description="README.md",
    long_description_content_type="text/markdown",
    url="https://github.com/toasterparty/mp2hudcolor",
    author="toasterparty",
    author_email="toasterparty@derpymail.org",
    license="MIT",
    packages=find_packages(),
    ext_modules=extensions,
    cmdclass={"build_ext": build_ext},
)
