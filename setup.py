from setuptools import setup, find_packages

setup(
    name="legal_ai_agent",
    version="0.1.0",
    description="Legal AI Agent для аналізу та генерації юридичних документів",
    author="Ваше Ім’я",
    packages=find_packages(exclude=["tests*"]),
    include_package_data=True,
    install_requires=[
        "streamlit>=1.25.0",
        "requests",
        "pandas",
        "langchain",
        "openpyxl",
        "python-dotenv",
        "prometheus-client",
    ],
    entry_points={
        "console_scripts": [
            "legal-agent=cli:main",
        ],
    },
)
