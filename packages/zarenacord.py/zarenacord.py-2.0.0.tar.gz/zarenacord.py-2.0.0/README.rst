zarenacord.py
==============

.. image:: https://discord.com/api/guilds/456574328990072838/embed.png
   :target: https://discord.gg/SwfNRrmr3p
   :alt: Discord server invite
.. image:: https://img.shields.io/pypi/v/zarenacord.py.svg
   :target: https://pypi.python.org/pypi/zarenacord.py
   :alt: PyPI version info
.. image:: https://img.shields.io/pypi/pyversions/zarenacord.py.svg
   :target: https://pypi.python.org/pypi/zarenacord.py
   :alt: PyPI supported Python versions

A modern, easy to use, feature-rich, and async ready API wrapper for Discord written in Python.

**PLEASE NOTE: This lib is a fork of OG discord.py by Rapptz! Since Danny no longer maintains dpy so I created this in order to add any upcoming feature by Discord.**

Key Features
-------------

- Modern Pythonic API using ``async`` and ``await``.
- Proper rate limit handling.
- Optimised in both speed and memory.

Installing
----------

**Python 3.8 or higher is required**

To install the library without full voice support, you can just run the following command:

.. code:: sh

    # Linux/macOS
    python3 -m pip install -U zarenacord.py

    # Windows
    py -3 -m pip install -U zarenacord.py

Otherwise to get voice support you should run the following command:

.. code:: sh

    # Linux/macOS
    python3 -m pip install -U "zarenacord.py[voice]"

    # Windows
    py -3 -m pip install -U zarenacord.py[voice]


To install the development version, do the following:

.. code:: sh

    $ git clone https://github.com/Zarenalabs/zarenacord.py.git
    $ cd zarenacord.py
    $ python3 -m pip install -U .[voice]


Optional Packages
~~~~~~~~~~~~~~~~~~

* `PyNaCl <https://pypi.org/project/PyNaCl/>`__ (for voice support)

Please note that on Linux installing voice you must install the following packages via your favourite package manager (e.g. ``apt``, ``dnf``, etc) before running the above commands:

* libffi-dev (or ``libffi-devel`` on some systems)
* python-dev (e.g. ``python3.6-dev`` for Python 3.6)

Quick Example
--------------

.. code:: py

    import discord

    class MyClient(discord.Client):
        async def on_ready(self):
            print('Logged on as', self.user)

        async def on_message(self, message):
            # don't respond to ourselves
            if message.author == self.user:
                return

            if message.content == 'ping':
                await message.channel.send('pong')

    client = MyClient()
    client.run('token')

Bot Example
~~~~~~~~~~~~~

.. code:: py

    import discord
    from discord.ext import commands

    bot = commands.Bot(command_prefix='>')

    @bot.command()
    async def ping(ctx):
        await ctx.send('pong')

    bot.run('token')

Links
------

- `Documentation <https://discordpy.readthedocs.io/en/latest/index.html>`_
- `Official zarenacord Server <https://discord.gg/r3sSKJJ>`_
- `Discord API <https://discord.gg/discord-api>`_
