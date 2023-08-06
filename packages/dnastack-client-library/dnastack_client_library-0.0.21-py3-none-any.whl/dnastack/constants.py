import os


cli_directory = f"{os.path.expanduser('~')}/.dnastack"
config_file_path = f"{cli_directory}/config.yaml"
downloads_directory = f"{os.getcwd()}"

ACCEPTED_CONFIG_KEYS = [
    "data-connect-url",
    "collections-url",
]
