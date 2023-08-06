# Fabric Tasks to simplify deployment on our servers

To use these features, create a `fabfile.py` at the same level as your manage.py.
Add the following code:

    from danemco_fabric import *

    configure()

Run `fab` and a site.conf file will be generated for you. You can adjust this as needed.

The [DEFAULT] section of site.conf can be read/written from autosite.

# Setting Python Version

You can change your projects python binary for the virtualenv by setting the `python = python_binary` configuration of your `site.conf` file.

**Note:** If the python setting is not present then the virtualenv will be built with the default version of python for the operating system.  

### Example

```
[DEFAULT]
virtualenv = ./venv-productionlogging
name = reports.productionlogging.com
server = sirius-b
test_modules =
branch = master
path = /var/www/reports.productionlogging.com
settings = project.settings.production
requirements = requirements/production.txt
deploy-cronjobs = False
exclude_media=*.pdf,*.zip,*.txt,*.csv,*.las
python = python3.4
```   

# Management Commands

In order to utilize management commands defined in this project you must add `danemco_fabric` to the `INSTALLED_APPS` configuration within your `settings.py` file.

Available commands: `clear_cache`

### `deploy.clearcache`: `clear_cache`

This is a Django management command which can be run remotely using the fabric command: `fab deploy.clearcache`.

#### Manual Refresh

Run the command and pass a positional argument or a keyword argument, `key` using fabric syntax. The value should be a single string key or a comma separated string of keys:

```
$ fab deploy.clearcache:default,mycache,another-cache
```

```
$ fab deploy.clearcache:key=default,mycache,another-cache
```

#### Refresh via `site.conf`

**NOTE:** If this second option is enabled, it will automatically clear the cache(s) when running `fab.deploy` or `fab.restart`. *Default:* **None**.

Add an opt in configuration value to your `site.conf` to set the default caches to clear:

```
#site.conf
#...
clear_caches = True
# OR
clear_caches = default,custom-cache,templates,etc
```

# Testing

This project uses Tox to process tests on multiple environments. Currently it supports the following:

- Python 2.7: Tox environment `-e py27`
- Python 3.8: Tox environment `-e py38`

If you wish to run all tests locally for all environments, enter the following in your terminal:

```bash
./tox_build.sh
```

If you wish to run the tests locally for a specific environment, enter the following in your terminal:

```bash
./tox_build.sh -e py27
```

If you need to rebuild the environment(s), you can pass the `--recreate` flag to the `tox_build.sh` command.

```bash
./tox_build.sh --recreate;
# Or
./tox_build.sh -e py38 --recreate;
```
