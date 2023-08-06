import setuptools


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="worldguard_api",
    version="0.0.1",
    description="Minecraft WorldGuard API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.cofob.ru/cofob/worldguard_api",
    install_requires=["mysql-connector-python"],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
