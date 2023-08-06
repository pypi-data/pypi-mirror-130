from distutils.core import setup

import setuptools

setup(
    name="vittawhatsapp",
    packages=setuptools.find_packages(),
    version="1.8",
    license="MIT",
    description="VittaWhatsapp é uma simples ferramenta para automação de Whatsapp",
    author="Fabricio Roney de Amorim",
    author_email="fabriciomrm@outlook.com",
    url="https://github.com/fabriciomrm/vittawhatsapp",
    download_url="https://github.com/fabriciomrm/vittawhatsapp.git",
    keywords=["sendwhatmsg", "info", "playonyt", "search", "watch_tutorial"],
    install_requires=["pyautogui", "wikipedia", "requests", "Pillow"],
    include_package_data=True,
    long_description="README.md",
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
