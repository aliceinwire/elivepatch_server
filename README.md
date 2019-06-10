# elivepatch-server
[![Build Status](https://travis-ci.org/gentoo/elivepatch-server.svg?branch=master)](https://travis-ci.org/gentoo/elivepatch-server)
![Maintainability](https://api.codeclimate.com/v1/badges/d79ff85d840722dbc9d6/maintainability)](https://codeclimate.com/github/gentoo/elivepatch-server/maintainability)

Flexible Distributed Linux Kernel Live Patching


## Setup
`elivepatch-server` is a [flask](https://www.palletsprojects.com/p/flask/)-based application.

You can use [virtualenv](https://virtualenv.pypa.io/en/stable/) to have a separate python3 environment.
``` sh
$ cd elivepatch-server
$ virtualenv .venv
$ source .venv/bin/activate
$ pip install -r requirements
```

``` sh
$ python elivepatch-server
```

Will run the server using [werkzeug](https://palletsprojects.com/p/werkzeug/)

## API

- Endpoint root: /elivepatch/api/
- agent: /elivepatch/api/v1.0/agent
- send_livepatch: /elivepatch/api/v1.0/send_livepatch
- GetFiles: /elivepatch/api/v1.0/get_files

More information on the REST API is [here](docs/API.md)
