from setuptools import find_packages, setup

INSTALL_REQUIRES = [
    "numpy",
    "optuna",
    "pyarrow",
    "pydantic",
    "joblib",
    "pandas",
    "scikit-learn",
    "lightgbm",
    "logger"
]

with open("README.md") as f:
    long_description = f.read()

if __name__ == "__main__":
    setup(
        name="kaggle-autolgb",
        version="0.0.6",
        description="tune with optuna and model LightGBM",
        long_description=long_description,
        long_description_content_type="text/markdown",
        author="Aditta Das Nishad",
        author_email="nishad009adi@gmail.com",
        install_requires=INSTALL_REQUIRES,
        platforms=["linux", "unix"],
        python_requires=">=3.6",
        package_dir={"": "src"},
        packages=find_packages("src"),
        url="https://github.com/Aditta-das/kaggle-autolgb.git"
    )