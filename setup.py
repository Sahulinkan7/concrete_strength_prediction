from setuptools import setup, find_packages

HYPHEN_E_DOT = "-e ."


def get_requirements(filepath):
    with open(filepath, "r") as file:
        requirements = file.readlines()
        requirements = [r.replace("\n", "") for r in requirements]
        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)
        print(requirements)
        return requirements


setup(
    name="concrete_compresive_strength_prediction",
    author="Linkan kumar sahu",
    author_email="sahulinkan7@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements("requirements.txt"),
)
