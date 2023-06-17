file:    Readme-3.0.md<br>
author:  rbw<br>
date:    Sun May 28 13:38:47 EDT 2023
purpose: Enhancements to enable analysis with Python Data Science tools<br>

Note: as of Feb 13, 2021, all new development of this version 2.0 switched
to version 3.0.

Version 2.0 polls a number of RSS Feeds, saves the original RSS files,
and dedups the text and saves to a format similar to JSON.
There was an effort to send text to a Kafka topic and to incorporate
NiFi, which should either be completed or removed.

The goals of this version -- version 3.0 -- are to:
1. Use Pycharm and/or VSCode as development environment
1. Convert from Python 2 to Python 3
1. Produce JSON output
1. Clean up text (convert characters such as "&#038;")
1. Downstream analysis, using Spacy, Hugging Face, etc.
1. Find issue of process halting ~monthly
1. Use dynaconf to manage configuration parameters; maintain parameters
in "settings.toml", ".secrets.toml", and ".env"
1. Set Python root directory, and import libraries relative to that
directory ("import a.b.function")
1. Produce JSON output
1. Manage processes with Linux systemctl
1. Convert archived data to JSON
1. Log errors using Python logging, write log files to /var/log/cn_rss_poller/
1. Generate metrics, manage using ??? tools

<h3>Notes</h3>
1. Store all python artifacts and dependencies in directory "venv/".
<br/>pip freeze > ./requirements.txt
<br/>pip -r ./requirements.txt
1. Use standard Python directory structure:
<br/>
```https://docs.python-guide.org/writing/structure/```
