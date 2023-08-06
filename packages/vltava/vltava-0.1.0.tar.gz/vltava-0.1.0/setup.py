# majka==0.8
# pytest==6.2.4
# ufal.morphodita==1.10.1.1
# gensim==4.0.1
import setuptools

VERSION = "0.1.0"

INSTALL_REQUIRES = [
    "majka>=0.8",
    "ufal.morphodita>=1.10.1.1",
    "gensim>4",
]

EXTRAS_REQUIRE = {
    "tests": ["pytest"]
}


def run_setup():
    """
    Runs the package setup.
    """

    setup_params = {
        "name": "vltava",
        "version": VERSION,
        "description": "Opinionated Czech Language Processing",
        "author": "Jan Cervenka",
        "author_email": "jan.cervenka@yahoo.com",
        # "package_dir": "vltava",
        "packages": ["vltava"],
        "python_requires": ">=3.7",
        "install_requires": INSTALL_REQUIRES,
        "extras_require": EXTRAS_REQUIRE

        }
    setuptools.setup(**setup_params)


if __name__ == '__main__':
    run_setup()
