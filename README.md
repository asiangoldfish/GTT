# Git Time Tracker
*Git Time Tracker* is a tool to track a groups time usage per issue. This is tailored toward SCRUM or similar methodologies in small teams.

Currently, only GitLab is supported.



## Background
At the time of creating *GTT*, GitLab v.18.5 does not support tracking tasks not associated with an issue or epic, and visualising time log. Teams who depend on GitLab's time tracker to record time performance and deviations between estimated and actual time usage, must refer to external tools.

*GTT* was written as an internal tool to fulfill the following requirements:
- Easy to use for non-programmers and as a command-line tool.
- Visualise time on different basis, e.g.
    - per-author
    - per-issue or epic
- Visualise time in different formats, e.g.
    - table
    - bars
    - pie chart

The most important goal is to be a tool to help contributors measure their own performance and time estimations.

It is fully open-source licensed under [Apache 2.0](./LICENSE).

## Prerequisites
Prerequisites
- `python` version 3.11
    - Other Python versions may work, but is not tested. GTT's code may be introduced to breaking changes for unsupported Python versions.
- `python-venv`
    - `python-venv` is used only for the virtual environment. Most other solutions, like `virtual-env` and `anaconda`, should work.

## Getting Started
The project currently do not have any releases. Therefore, it is recommended to use Git to clone the project, or to download it as a ZIP archive on GitHub.

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

The project uses `argparse` and supports subcommands. Example:
```sh
# Default help page
gtt.py --help

# Help page for time-deviation command
gtt.py time-deviation --help
```

## Examples
*Compute deviation between esimated time usage and time spent in sprint n*

```
gtt.py time-deviation --sprint=n --user='Your name'
```

## Tokens
You will normally not be able to consume protected APIs without some kind of verification. The most common verification method is to generate a token with the vendor's solution and include it in the request header. For GitLab specifically, one of the following scopes must be enabled:
- ai_workflows
- api
- read_api

