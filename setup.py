from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="techmart-vulnerable-lab",
    version="1.0.0",
    author="Security Research Team",
    author_email="security@example.com",
    description="A realistic vulnerable e-commerce platform for security education and training",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/security-labs/techmart-vulnerable-lab",
    project_urls={
        "Bug Tracker": "https://github.com/security-labs/techmart-vulnerable-lab/issues",
        "Documentation": "https://github.com/security-labs/techmart-vulnerable-lab/wiki",
        "Source Code": "https://github.com/security-labs/techmart-vulnerable-lab",
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Education",
        "Intended Audience :: Information Technology",
        "Topic :: Security",
        "Topic :: Education :: Testing",
        "License :: Other/Proprietary License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Operating System :: OS Independent",
        "Environment :: Web Environment",
        "Framework :: Flask",
    ],
    packages=find_packages(exclude=["tests*", "docs*"]),
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
        "docker": [
            "gunicorn>=21.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "techmart-lab=app:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["templates/*", "static/*", "database/*"],
    },
    keywords=[
        "security",
        "education", 
        "penetration-testing",
        "vulnerability-assessment",
        "web-security",
        "owasp",
        "cybersecurity",
        "training",
        "flask",
        "vulnerable-application"
    ],
)
