# TepezzaScraper

## Motivation/use case
Get a list of doctors and their metadata from www.tepezza.com/ted-specialist-finder, which is unfortunately ReCaptcha-protected.

## Mechanism of action
A user enters zip codes and the program uses tshark to monitor the JSON sent back.

## Requirements
* All third-party python packages that pip requires for the package download
* tshark
* Python 3.8+

## Configuration
See [DEFAULT_CONF.ini](DEFAULT_CONF.ini) for the default; otherwise pass custom args to the constructor of `TepezzaApi`.