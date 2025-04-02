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

If you truly want to understand the ins and outs of git submodules, read this blog post > https://www.cyberdemon.org/2024/03/20/submodules.html (also [archived](https://archive.is/Q3QOz))

## Developing on Splunk-soar

Execute the following commands and you'll see how to build the package.

```shell
python -m venv venv
# activate venv
pip install -r requirements.txt
inv --list  # gives you all commands that you can run.
```

## Testing

We have no unittests for splunk-soar as we can't really break it down into units. So we're left with pure integration tests. In `test_action_inclusion`, we do assert that all actions have test method associated with them.

To run the integration tests start splunk-soar in smeden. The start of the instance takes at least 30min.

```
@smeden create_int splunk_soar dev current 72
```

Once splunk is started you need to get an auth token to the instance. You'll find this auth token in `Administration > User Managment > Users > Add User > Select automation`. There may already be an automation user, in which case you can use the token from there. The automation user needs the role `Observer` to work.

Set the environment variables.
```
export PHOST="in-1137a.recfut.net"
export PTOK=<token>
export RF_TOKEN=<token>
```
