# Q-CTRL Python Cirq

The aim of the Q-CTRL Cirq Adapter package is to provide export functions allowing
users to deploy established error-robust quantum control protocols from the
open literature and defined in Q-CTRL Open Controls on Google quantum devices
and simulators.

Anyone interested in quantum control is welcome to contribute to this project.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [Credits](#credits)
- [License](#license)

## Installation

Q-CTRL Cirq Adapter can be installed through `pip` or from source. We recommend
the `pip` distribution to get the most recent stable release. If you want the
latest features then install from source.

### Requirements

To use Q-CTRL Cirq Adapter you will need an installation of Python. We
recommend using the [Anaconda](https://www.anaconda.com/) distribution of
Python. Anaconda includes standard numerical and scientific Python packages
which are optimally compiled for your machine. Follow the [Anaconda
Installation](https://docs.anaconda.com/anaconda/install/) instructions and
consult the [Anaconda User
guide](https://docs.anaconda.com/anaconda/user-guide/) to get started.

We use interactive jupyter notebooks for our usage examples. The Anaconda
python distribution comes with editors for these files, or you can [install the
jupyter notebook editor](https://jupyter.org/install) on its own.

### Using PyPi

Use `pip` to install the latest version of Q-CTRL Cirq Adapter.

```shell
pip install qctrl-cirq
```

### From Source

The source code is hosted on
[Github](https://github.com/qctrl/python-cirq). The repository can be
cloned using

```shell
git clone git@github.com:qctrl/python-cirq.git
```

Once the clone is complete, you have two options:

1. Using setup.py

   ```shell
   cd python-cirq
   python setup.py develop
   ```

   **Note:** We recommend installing using `develop` to point your installation
   at the source code in the directory where you cloned the repository.

1. Using Poetry

   ```shell
   cd python-cirq
   ./setup-poetry.sh
   ```

   **Note:** if you are on Windows, you'll need to install
   [Poetry](https://poetry.eustace.io) manually, and use:

   ```bash
   cd python-cirq
   poetry install
   ```

Once installed via one of the above methods, test your installation by running
`pytest`
in the `python-cirq` directory.

```shell
pytest
```

## Usage

See the [Jupyter notebooks](examples).

## Contributing

For general guidelines, see [Contributing](https://github.com/qctrl/.github/blob/master/CONTRIBUTING.md).

### Building documentation

Documentation generation relies on [Sphinx](http://www.sphinx-doc.org).

To build locally:

1. Ensure you have used one of the install options above.
1. Execute the make file from the docs directory:

    If using Poetry:

    ```bash
    cd docs
    poetry run make html
    ```

    If using setuptools:

    ```bash
    cd docs
    # Activate your virtual environment if required
    make html
    ```

The generated HTML will appear in the `docs/_build/html` directory.

## Credits

See
[Contributors](https://github.com/qctrl/python-cirq/graphs/contributors).

## License

See [LICENSE](LICENSE).
