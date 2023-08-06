# DNAstack Client Library
`dnastack` (formerly `clippe` (RIP 2021-2021)) is the command line interface and Python library for DNAstack products

This project is written in Python and uses the [Click](https://click.palletsprojects.com/en/7.x/). The documentation is really nice so make sure to have a look if you're running into any problems developing.

## Getting Started

### Running the CLI locally
1. Run `pip3 install -r requirements.txt` to download all the dependencies
2. From the command line run `python3 -m dnastack ...`

#### Examples
```
python3 -m dnastack --help

python3 -m dnastack config set data-connect-url https://collection-service.publisher.dnastack.com/collection/library/search/

python3 -m dnastack dataconnect tables list

python3 -m dnastack dataconnect tables get covid.cloud.variants

python3 -m dnastack dataconnect query "SELECT drs_url FROM covid.cloud.files LIMIT 10"
```

### Using the CLI as a Python library
The CLI can also be imported as a Python library. It is hosted on PyPi here: https://pypi.org/project/dnastack/

You can simply install it as a dependency with `pip3 install dnastack-client-library` or through other traditional `pip` ways (e.g. `requirements.txt`)

To use the `dnastack-client-library` library in Jupyter Notebooks and other Python code, simply import the PublisherClient object

`from dnastack import PublisherClient`

#### Example

```python
from dnastack import PublisherClient

publisher_client = PublisherClient(dataconnect_url='[DATACONNECT_URL]')


# get tables
tables = publisher_client.dataconnect.list_tables()

# get table schema
schema = publisher_client.dataconnect.get_table('[TABLE_NAME]')

# query
results = publisher_client.dataconnect.query('SELECT * FROM ...')

# load a drs resource into a DataFrame
drs_df = publisher_client.load(['[DRS_URL]'])

# download a DRS resource into a file
publisher_client.download(['[DRS_URL]'])
```

## Distributing the CLI/Python library

### Installing `pyenv-virtualenv`

In order to standardize the build environment for the CLI, we use the `pyenv-virtualenv` command line tool.

To install, follow the instructions listed [here](https://github.com/pyenv/pyenv-virtualenv)

To create the environment to build:

```bash
env PYTHON_CONFIGURE_OPTS="--enable-framework" pyenv install 3.9.0
pyenv virtualenv 3.9.0 dnastack-cli
```

To use the environment, run `pyenv activate dnastack-cli`.

To exit the environment, run `pyenv deactivate`

**Note**: The build scripts already make calls to the `activate` and `deactivate` commands sp they should only be used for manual builds.

### Distributing as a CLI
For convenience, we have added scripts in the `scripts` directory to automate all of the distribution.

To build and/or publish the CLI,
1. If you are creating or pushing to a release, you must set the `GITHUB_TOKEN` environment variable to your Github Account token (instructions for creating a token are [here](https://docs.github.com/en/github/authenticating-to-github/keeping-your-account-and-data-secure/creating-a-personal-access-token)).
2. Run the following command based on the build
```bash
./build-cli.sh
\  --help / -h
\  --mac / -m              [Build the Mac Executable]
\  --windows / -w          [Build the Windows Executable]
\  --linux / -l            [Build the Linux Executable]
\  --release / -r          [Release to Github Releases]
\      --release-version=[RELEASE VERSION] (Required for release)
\      --release-title=[RELEASE TITLE]
\      --release-desc=[RELEASE DESCRIPTION]
```

More detailed instructions on the CLI distribution can be found [here](docs/distribution.md)

### Distributing as a Python Library

The python library is distributed on PyPI, a package manager for Python. Like the CLI, we have provided a script to build and deploy the library.

To deploy to PyPI:
1. Set the `PYPI_API_TOKEN` environment variable to your PyPI account's personal access token (information on getting a PyPI token [here](https://pypi.org/help/#apitoken))
2. Run `./scripts/deploy-pip.sh`

More detailed instructions on the CLI distribution can be found [here](docs/pypi.md)

## API References

**Note:** These references are not complete and very much a work in progress.

CLI: [CLI Reference](docs/reference/cli.md)


## Client Configurations

In the CLI, we use Wallet clients in order to authorize users to access Data Connect and DRS functionality.

Information on creating a client and exisitng configurations can be found [here](docs/clients.md)


## Testing

There are e2e-tests set up for the CLI. Instructions to run can be found [here](docs/e2e-tests.md)
