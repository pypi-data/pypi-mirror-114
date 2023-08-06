# django-autosecretkey

autosecretkey is a simple reusable Django app which will make it easier to
distribute your Django project by taking care of generating a secure SECRET_KEY
and storing it outside of your project's settings.py

## Quick start

1. In your project's settings.py, import the app like so:

   ```from autosecretkey import AutoSecretKey```

2. Still in the settings.py file, replace the existing SECRET_KEY line with
   something like this:

   ```SECRET_KEY = AutoSecretKey(BASE_DIR / "config.ini").secret_key```

   (N.B.: Of course, this line has to be after the BASE_DIR line.)

   This will store the key in a file called `config.ini` in your project's base
   directory (i.e. the one containing `manage.py`).

   Make sure not to ship this file with your code distribution. For example,
   you may want to add it to your .gitignore file if you publish the project in
   a git repository.

## Additional configuration

For additional security, you may want to store your secret key in a different
location than your project's base directory. You could, for example, do
something like this:

```AutoSecretKey("/etc/your_project/configuration")```

You need to manually make sure that the user your Django project runs as has
the permission to read and write this file. Running something like this as
root should do the trick in Linux (replacing "djangouser" with the actual user
name):

```
mkdir /etc/your_project/
touch /etc/your_project/configuration
chown djangouser /etc/your_project/configuration
```

In the end, this is just a simple wrapper around configparser.ConfigParser, so
you can store custom configuration values in the file that holds your secret
key. You can access the ConfigParser object as the `config` attribute of your
AutoSecretKey object.

This is a simple example you could have in your `settings.py`:

```
from autosecretkey import AutoSecretKey
my_config_file = AutoSecretKey(BASE_DIR / "config.ini")
SECRET_KEY = my_config_file.secret_key
TIME_ZONE = my_config_file.config["MY_SETTINGS"]["TIME_ZONE"]
```

For reference, the corresponding `config.ini` might look like this:

```
[AutoSecretKey]
SecretKey = WellThisIsWhereYouWillFindYourSecretKey

[MY_SETTINGS]
TIME_ZONE = UTC
```

All methods you can use on any other ConfigParser object can be used on that
object as well, of course, like get(), getboolean(), etc. For convenience, you
can use the AutoSecretKey object's update() method to re-read the contents of
the config file, and the write() method to write back any changes you have made
on the object to the configuration file.

Note that the ConfigParser behaves like a RawConfigParser in that it does not
support interpolation.