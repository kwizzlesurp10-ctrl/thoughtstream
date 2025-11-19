from setuptools import setup, find_packages

setup(
    name="thoughtstream",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "ollama",
        # "sqlite-vss", # Not easily available on Windows via pip
        "pynput",
        "pyperclip",
        "rich",
        "typer",
        "pyyaml",
        "cryptography",  # For encryption
        "aiohttp",
    ],
    entry_points={
        "console_scripts": [
            "thoughtstream=thoughtstream.daemon:app",
        ],
    },
)

