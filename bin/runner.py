import subprocess
import os
from decodeon.core import settings
from decodeon.types.enums import EnvironmentEnum


def run():
    # Set the app based on the environment
    if settings.environment == EnvironmentEnum.development:
        reload = True
        host = "127.0.0.1"
    else:
        reload = False
        host = "0.0.0.0"

    # Command to run Streamlit from a Python script
    command = [
        "streamlit",
        "run",
        os.path.abspath("src/decodeon/main.py"),  # Path to your Streamlit script
        "--server.port",
        str(settings.port),
        "--server.address",
        host,
    ]

    # If development mode, enable reloading
    if reload:
        command.append(
            "--server.enableCORS=false"
        )  # This can help with certain CORS issues in development

    # Run the Streamlit app
    subprocess.run(command)


if __name__ == "__main__":
    run()
