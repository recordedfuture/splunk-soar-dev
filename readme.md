# Splunk soar dev

## Get started

This repo contains tests and dev tooling to make it a pleasant experience to develop for Splunk soar.

To start to work with splunk soar. Take the following steps.

```shell
git clone <this repo>
git submodule init
git submodule update # fetches the latest commits from submodule repo
```

When making changes to the submodule (splunk-soar), cd into the directory and commit your changes there.

## Developing on Splunk-soar

```shell
python -m venv venv
# activate venv
pip install -r requirements.txt
inv --list  # gives you all commands that you can run.
```
