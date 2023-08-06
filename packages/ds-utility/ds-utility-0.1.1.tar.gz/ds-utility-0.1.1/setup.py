from itertools import chain
from pathlib import Path

from setuptools import find_packages, setup

here = Path(__file__).parent

requirements_path = here / "requirements" / "prod.txt"


def read_requirements(path):
    try:
        with path.open(mode="rt", encoding="utf-8") as fp:
            return list(filter(None, (line.split("#")[0].strip() for line in fp)))
    except IndexError:
        raise RuntimeError(f"{path} is broken")


extras_require = {
    "mlflow": ["scikit-learn", "mlflow"],
    "plot": ["matplotlib"],
}

extras_require["all"] = list(chain(*extras_require.values()))

setup(
    name="ds-utility",
    version="0.1.0",
    description="Utility functions for Data Science related works.",
    python_requires=">=3.9.0",
    setup_requires=["setuptools_scm"],
    install_requires=read_requirements(requirements_path),
    extras_require=extras_require,
    download_url="https://github.com/skshahidur/ds-utility/archive/refs/tags/0.1.0.tar.gz",  # TODO: check usage for CD
    keywords=["DSUTILS", "DSUTILITIES", "DATASCIENCEUTILITY", "DATASCIENCEUTILITIES"],
    use_scm_version={
        "version_scheme": "guess-next-dev",
        "local_scheme": "dirty-tag",
        "write_to": "src/ds_utility/_repo_version.py",
        "write_to_template": 'version = "{version}"\n',
        "relative_to": __file__,
    },
    include_package_data=True,
    package_data={},
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    entry_points={"console_scripts": ["ds_utility = ds_utility.cli:entrypoint"]},
    author="skshahidur",
    author_email="skshahidur@gmail.com",
    url="https://www.linkedin.com/in/skshahidur/",
)
