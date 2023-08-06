from setuptools import setup, find_packages
import requests
import semantic_version

install_requires = [
    'requests==2.25.1',
]

setup(
        name="cloudflare_workers",
        version="0.0.1",
        author="Dinesh Sonachalam",
        author_email="dineshsonachalam@gmail.com",
        description="A simple Python wrapper to Cloudflare Workers",
        url="https://github.com/dineshsonachalam/cloudflare_workers",
        long_description=open('README.md').read(),
        long_description_content_type='text/markdown',
        zip_safe=False,
        license='MIT',
        keywords='cloudflare workers',
        python_requires=">=3.1",
        install_requires=install_requires,
        packages=find_packages(),
        classifiers=[
                "Programming Language :: Python :: 3",
                "License :: OSI Approved :: MIT License",
                "Operating System :: OS Independent",
        ]
)