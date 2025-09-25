# Git Time Tracker
*Git Time Tracker* is a tool to track a groups time usage per issue. This is tailored toward SCRUM or similar methodologies in small teams.

Currently, only GitLab is supported.

## Usage
Prerequisites:
- Python version 3.11
- python-venv

Other Python versions may work, but is not tested. GTT's code may be introduced to breaking changes for unsupported Python versions.

`python-venv` is used only for the virtual environment. Most other solutions, like `virtual-env` and `anaconda`, should work.

1. Clone the project and install dependencies.
    ```
    git clone https://github.com/asiangoldfish/GTT.git
    cd GTT
    python -m venv .venv
    source .venv/bin/activate
    ```
2. Configure environment and secrets
    ```
    cp .env.template .env
    ```

The `.env` contains both secrets and various environment variables. This should NOT be version controlled.
- `TOKEN`: The private token to access your account (i.e. GitLab). See [Tokens](#tokens) for more info.
- `PROJECT_ID`: A unique identifier for the project or repositories. This may be hard to find. You can perhaps find it in the web page's source code, as described in this [Stack Overflow post](https://stackoverflow.com/a/45500237).
- `VENDOR_URL`: The provider's URL, like https://github.com or https://gitlab.com.

## Tokens
You will normally not be able to consume protected APIs without some kind of verification. The most common verification method is to generate a token with the vendor's solution and include it in the request header. For GitLab specifically, one of the following scopes must be enabled:
- ai_workflows
- api
- read_api

