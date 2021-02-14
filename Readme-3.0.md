One          | Two<br>
------------ | -------------<br>
file:    Readme-3.0.md<br>
author:  rbw<br>
date:    Sat, Feb 13, 2021  6:54:20 PM<br>
purpose: Enhancements to enable analysis with Python Data Science tools<br>

Note: as of Feb 13, 2021, all new development of this version 2.0 switched
to version 3.0.

Version 2.0 polls a number of RSS Feeds, and sends the de-duped text to
a Kafka topic and incorporates NiFi.

The goals of this version -- version 3.0 -- are to:
1. Convert from Python 2 to Python 3
1. Produce JSON output
1. Log errors
1. Generate metrics
1. Convert archived data to JSON


