# Samtec Device Connect Service

A Python 3 SDC conforming REST API to run on IoT devices that enables user discovery, viewing, and management.

## Installation

```bash
pip install samtecdeviceshare
```

## Running

First ensure all environment variables are set correctly.
Note: To test locally for development ensure EMULATION and PYTHON_ENV are set.

```bash
python -m samtecdeviceshare.server
```

## Environment Variables

A number of environment variables are supported for configuration. These configurations can also be contained in a yaml/json configuration file specified using `SDC_CONFIGURATION_PATH`. Env vars take precedence over the configuration file.

### SDC Server / General

These variables are specific to this SDC service. The variables can also start with prefix `SDC_`.

| Name              | Description                   | Default                                     |
| ----------------- | ----------------------------- | ------------------------------------------- |
| REST_ADDRESS      | Rest API Address              | 0.0.0.0                                     |
| REST_PORT         | Rest port                     | 47546                                       |
| ROOT_PATH         | API root path                 | ''                                          |
| PYTHON_ENV        | enum: development production  | production                                  |
| EMULATION         | Use emulated devices/io       | null                                        |
| LOG_VERBOSE       | boolean verbose logs          | false                                       |

### Application

These variables are used to provide app info that will be shared by SDC.

| Name              | Description                   | Default                                     |
| ----------------- | ----------------------------- | ------------------------------------------- |
| APP_NAME          | Name of app                   | SDC App                                     |
| APP_VERSION       | SemVer of app                 | 0.0.0                                       |
| APP_WEB_PORT      | Embedded web app port         | 80                                          |
| APP_IMG_PATH      | app icon path                 | {CURDIR}../static/img.png                   |
| APP_LOG_PATH      | Path to store log files       | default tempdir()                           |
| APP_LOCK_PATH     | Path to update lock file      | .__sdc.lock                                 |

### Wireless Networks

SDC can handle configuring N wireless networks. Prefix *SDC_* is required. Us integer `i` in prefix for defining multiple networks.
A network can optionally be defined default. This will be primary method used to handle updates and will be exposed through REST API.

| Name                     | Description                   | Default                         |
| ------------------------ | ----------------------------- | ------------------------------- |
| SDC_WIFI[i]_SSID         | WiFi SSID                     | null*                           |
| SDC_WIFI[i]_MODE         | enum: HOTSPOT CLIENT DISABLED | DISABLED                        |
| SDC_WIFI[i]_PASS         | WiFi passphrase               | null                            |
| SDC_WIFI[i]_IFACE        | WiFi hardware interface       | null                            |
| SDC_WIFI[i]_DEFAULT      | Use as default for updates    | False                           |

### Wired Networks

SDC can handle configuring N wired networks. Prefix *SDC_* is required. Us integer `i` in prefix for defining multiple networks.
`SDC_ETH[i]_IFACE` or `SDC_ETH[i]_REGEX_IFACE` is required with the latter supporting regex matching. Be careful defining multiple networks with generic regular expression.
[Most Linux distros follow a predictable naming scheme for interfaces.](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/networking_guide/sec-understanding_the_predictable_network_interface_device_names). When searching for interfaces, a fullmatch is required `re.fullmatch()`.

| Name                        | Description                   | Default                      |
| --------------------------- | ----------------------------- | ---------------------------- |
| SDC_ETH[i]_IFACE            | Interface name (str)          | null                         |
| SDC_ETH[i]_REGEX_IFACE      | Interface name (regex)        | null                         |
| SDC_ETH[i]_METHOD           | Primary method                | WiredConnectionMethod.auto   |
| SDC_ETH[i]_TIMEOUT          | Timeout of primary            | 15                           |
| SDC_ETH[i]_FALLBACK         | Fallback method               | null                         |
| SDC_ETH[i]_FALLBACK_TIMEOUT | Timeout to get DHCP address   | -1                           |

### Balena

Refer to Balena [documentation](https://www.balena.io/docs/learn/develop/runtime/) for list and description of variables.

- BALENA_SUPERVISOR_API_KEY
- BALENA_APP_ID
- BALENA_DEVICE_TYPE
- BALENA
- BALENA_SUPERVISOR_ADDRESS
- BALENA_SUPERVISOR_HOST
- BALENA_DEVICE_UUID
- BALENA_API_KEY
- BALENA_APP_RELEASE
- BALENA_SUPERVISOR_VERSION
- BALENA_APP_NAME
- BALENA_DEVICE_NAME_AT_INIT
- BALENA_HOST_OS_VERSION
- BALENA_SUPERVISOR_PORT

## Development

### Installing

```bash
git clone git@bitbucket.org:samteccmd/samtecdeviceshare.git samtecdeviceshare
cd samtecdeviceshare
poetry install --dev
poetry shell
```

### Testing

First, run dummy Balena supervisor:

```bash
bash ./tests/dummy-supervisor.sh
```

Next, fire up REST server using uvicorn:

```bash
EMULATION=1 \
PYTHON_ENV="development" \
DEBUG=1 \
uvicorn samtecdeviceshare.server:app --reload --reload-dir ./samtecdeviceshare
```

**Interactive API docs** will be available: <http://127.0.0.1:8000/docs>

### Unit Tests

```bash
pylint --rcfile .pylintrc samtecdeviceshare
pytest
```
