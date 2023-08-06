#!/usr/bin/env python3
"""Command line program for 'mopidris', a MPRIS D-Bus interface for Mopidy.

Usage
=====

Call with:
    python3 mopidris

See the help with all options explained:
    python3 mopidris --help

See also:
    - https://pypi.org/project/mopidris
    - https://codeberg.org/sph/mopidris

Please report bugs at:
    - https://codeberg.org/sph/mopidris/issues


Configuration File
------------------

`mopidris` reads a configuration file `mopidris.conf` (by default from the
default place for the user's configurations). It has a simple `key = value`
format and the keys are explained in the output of `python3 mopidris --help`.


Required Packages
=================

dbus-next >= 0.2.3
mopidy-asyncio-client >= 3.0.1


Optional Packages
=================

`mopidris` makes use of the following optional package, if it can find them,
but it also works well without them:
    - aiorun
    - colored_traceback
    - colorlog

For more information see https://pypi.org/project/mopidris or
https://codeberg.org/sph/mopidris


Created on Sun Mar 28 18:18:06 2021


Copyright (C) 2021  Stephan Helma

This file is part of mopidris.

mopidris is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

mopidris is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with mopidris. If not, see <https://www.gnu.org/licenses/>.

"""

# Import colored_traceback, so that we have it available for all other imports
try:
    # https://github.com/staticshock/colored-traceback.py
    # sudo pip3 install colored-traceback
    import colored_traceback
except ImportError:
    pass
else:
    colored_traceback.add_hook()


import os
from pathlib import Path
import sys
import argparse
import logging

# Import aiorun or asyncio
try:
    import aiorun
except ImportError:
    logging.warning(
        "Module 'aiorun' is not available. "
        "You might experience unpleasant sideeffects - such as locked ports - "
        "when shutting down.")
    import asyncio

from mopidris import main_loop


logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(name)s: %(message)s',
    datefmt='%H:%M:%S')


# Default values for command line options
__HOST = 'localhost'
__PORT = 6680
__ATTEMPTS = 5
__TIMEOUT = 20
__INTERFACES = []
__LOGLEVEL = logging.getLevelName(logging.getLogger().level).lower()


def get_userconfigfile():
    """Get the user's default configuration name.

    Returns
    -------
    str
        The name of the default user's configuration file.

    """
    # Get our name
    name = Path(sys.argv[0]).name
    # Get location of user's configuration directory
    if sys.platform == 'win32':
        # Borrowed from https://github.com/barry-scott/config-path/
        import ctypes
        import ctypes.wintypes

        buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
        ctypes.windll.shell32.SHGetFolderPathW(
            0, 0x1a,    # CSIDL_APPDATA, Application Data
            0, 0,       # SHGFP_TYPE_CURRENT, want current, not default value
            buf)

        config_folder = Path(buf.value)

    elif sys.platform == 'darwin':
        config_folder = Path('~/Library/Application Support/')
    else:
        config_folder = Path(os.getenv('XDG_DATA_HOME', '~/.config/'))

    return config_folder.joinpath(name, f'{name}.conf')


def parse_args(modules=[]):
    """Parse the command line arguments.

    Parameters
    ----------
    modules : [str], optional
        A list with the names of the modules, for which command line
        arguments should be automatically created in the 'debug' group, to
        set their logging levels independently of the main logging level.
        The default is [].

    Returns
    -------
    argparse.Namespace, {str: int}
        argparse.Namespace:
            The parsed command line arguments.
        {str: int}:
            Logging levels for modules. The key is the module name and the
            value the logging level.

    """
    # Help formatter
    class LinebreakDescriptionHelpFormatter(argparse.HelpFormatter):
        """Formatter which retains any line breaks in descriptions."""

        def _fill_text(self, text, width, indent):
            import textwrap
            return '\n'.join([
                textwrap.fill(
                    self._whitespace_matcher.sub(' ', paragraph).strip(),
                    width,
                    initial_indent=indent,
                    subsequent_indent=indent)
                for paragraph in text.splitlines()])

    # Type checkers
    def positiveint(string):
        """Parse 'string' into a positive integer."""
        i = int(string)
        if i > 0:
            return i
        else:
            raise ValueError('integer must be >0')

    def readablefile(string):
        """Check if 'string' is a readable file."""
        file = Path(string)
        if file.expanduser().is_file():
            return file
        else:
            raise ValueError(
                f"File '{string}' does not exist or is not readable")

    #
    # Command line parser
    #

    parser = argparse.ArgumentParser(
        description='Connect a (remote) Mopidy instance to the local DBus.',
        epilog='Configuration file:\n'
               "Each line in the configuration file is a 'key = value' pair. "
               "The key is given in the description of each parameter "
               "and the value can be any valid value.\n"
               "Comments start with '#' and everything after is discarded.\n"
               "\n"
               "Copyright (C) 2021, licensed under GPL 3.0 or later.",
        formatter_class=LinebreakDescriptionHelpFormatter)

    config_file = get_userconfigfile()

    #
    # Common arguments
    #

    parser.add_argument(
        nargs='?', default=__HOST,
        dest='host', metavar='HOST',
        help='the remote host name or ip address '
             '(default: %(default)s, configfile key: %(dest)s)')

    parser.add_argument(
        '-p', '--port', default=__PORT,
        dest='port', metavar='PORT',
        type=positiveint,
        help='the port number Mopidy is listening on '
             '(default: %(default)s, configfile key: %(dest)s)')

    parser.add_argument(
        '-r', '--retries', default=__ATTEMPTS,
        type=int,
        dest='reconnect_attempts', metavar='ATTEMPTS',
        help='how often to retry to connect to Mopidy; if -1, retry forever '
             '(default: %(default)s, configfile key: %(dest)s)')

    parser.add_argument(
        '-t', '--timeout', default=__TIMEOUT,
        type=positiveint,
        dest='reconnect_timeout', metavar='TIMEOUT',
        help='how long to wait between reconnection attempts '
             '(default: %(default)s, configfile key: %(dest)s)')

    parser.add_argument(
        '-q', '--can-quit',
        action='store_true',
        dest='can_quit',
        help='it is possible to quit this program from an application; '
             'note, that the (remote) will keep running '
             '(default: %(default)s, configfile key: %(dest)s)')

    parser.add_argument(
        '-m', '--no-mangle',
        action='store_false',
        dest='mangle',
        help='do not split the Internet radio stream title at " - " '
             '(default: %(default)s, configfile key: %(dest)s)')

    parser.add_argument(
        '-c', '--config',
        type=readablefile,
        dest='config', metavar='FILE',
        help=f'read values from the configuration file '
             f'(default: {config_file}, a configfile key is not supported)')

    #
    # DBus Interfaces
    #

    group = parser.add_argument_group('DBus Interfaces')

    group.add_argument(
        '-i', '--interface', default=__INTERFACES,
        choices=['tracklist', 'playlists'], action='append',
        dest='interfaces', metavar='{tracklist,playlists}',
        help="activate additional 'org.mpris.MediaPlayer2' DBus interfaces "
             "(the 'org.mpris.MediaPlayer2' and "
             "'org.mpris.MediaPlayer2.Player' interfaces are always active) "
             "(configfile key: %(dest)s - use one line for each interface)")

    #
    # Debugging
    #

    group = parser.add_argument_group('Debugging')

    # Available loglevels
    loglevels = [level[1].lower()
                 for level in sorted(logging._levelToName.items())
                 if level[0] > 0]

    group.add_argument(
        '-d', '--debug', default=__LOGLEVEL,
        choices=loglevels,
        dest='debug',
        help='the general loglevel '
             '(default: %(default)s, configfile key: %(dest)s)')

    # Do it for all given modules
    for module in modules:
        module_short = module.split('_', 1)[0]
        group.add_argument(
            f'--debug-{module_short}',
            choices=loglevels,
            dest=f'debug_{module}',
            help=f"the loglevel for the '{module}' module "
                 f"(default: follows --debug argument, "
                 f"configfile key: %(dest)s)")

    #
    # Parse and process
    #

    # 1st pass to get the configuration file
    args = parser.parse_args()

    if args.config is not None:
        config_file = args.config
    try:
        # Parse the configuration file and build a dictionary with its values,
        # discarding all values, which are not command line parameters
        default_args = {}
        with open(config_file.expanduser()) as f:
            for line in f:

                # Remove comments
                line = line.split('#', 1)[0].strip()
                if not line:
                    # Empty line
                    continue

                # Get keys and values
                try:
                    key, value = [t.strip() for t in line.split('=', 1)]
                except ValueError:
                    parser.error(
                        f"In the configuration file, "
                        f"the line '{line}' is missing the '=' sign")
                # No empty values are allowed
                if not value:
                    parser.error(
                        f"In the configuration file, "
                        f"the line '{line}' is missing a value")
                # Add it to our default args
                if key in args:
                    if key in default_args:
                        # Append value
                        v = default_args[key]
                        if isinstance(v, list):
                            # Append value to existing list
                            default_args[key].append(value)
                        else:
                            # Make a list
                            default_args[key] = [default_args[key], value]
                    else:
                        # Store value
                        default_args[key] = value
                else:
                    parser.error(
                        f"The key '{key}' found in the configuration file "
                        f"is not supported")
        # This is not very elegant, but there is no stable argparse API to
        # check the action of an argument (we could only use
        # 'parser._actions'), but we have to ensure that 'interfaces' is a
        # list!
        try:
            if not isinstance(default_args['interfaces'], list):
                default_args['interfaces'] = [default_args['interfaces']]
        except KeyError:
            pass

        # Set the parser's default arguments
        parser.set_defaults(**default_args)

    except FileNotFoundError:
        # Since argparse checked the existence for a user supplied
        # configuration file for us, this can only happens, if either
        #   - the default file should be used, but it does not exist, or
        #   - the user supplied file vanished between checking and opening
        # The first cause is ok, and we do not care about the second.
        pass

    except PermissionError as e:
        print(f'Could not open the configuration file.\n{e}', file=sys.stderr)
        exit(1)

    # 2nd pass, now that we have injected values from the configuration file
    args = parser.parse_args()

    # Remove the configuration file from the args namespace, because we
    # have dealt with it
    delattr(args, 'config')

    # mopidy_asyncio_client.MopidyClient requires 'None' and not negative
    # integer for infinite reconnection attempts
    if args.reconnect_attempts < 0:
        args.reconnect_attempts = None

    # Convert loglevel name for 'debug' to a numeic value
    args.debug = getattr(logging, args.debug.upper())

    # Transfer the modules' loglevels from the argparse.Namespace to a
    # separate dictionary (and convert it to number)
    module_loglevels = {}
    for module in modules:
        level = getattr(args, f'debug_{module}')
        if level is not None:
            # Store numeric loglevel for module, if given
            module_loglevels[module] = getattr(logging, level.upper())
        # Remove the attribute from the args namespace
        delattr(args, f'debug_{module}')

    return args, module_loglevels


if __name__ == '__main__':

    #
    # Process command line arguments
    #

    # Modules we want be able to change their logging level
    modules = ['mopidy_asyncio_client', 'dbus_next', 'websockets', 'aiorun',
               'interfaces.base', 'interfaces.root', 'interfaces.player',
               'interfaces.tracklist', 'interfaces.playlist']
    args, modules_loglevels = parse_args(modules=modules)

    #
    # Set loglevels (and minimum loglevel)
    #

    # Main logger
    loglevel_min = args.debug
    logging.getLogger().setLevel(args.debug)
    logging.info(
        'Loglevel set to: %s',
        logging.getLevelName(args.debug))

    # Module loggers
    for module, loglevel in modules_loglevels.items():
        loglevel_min = min(loglevel_min, loglevel)
        # Set loglevel for module, if given
        logging.getLogger(module).setLevel(loglevel)
        logging.info(
            "Loglevel for module '%s' set to: %s",
            module, logging.getLevelName(loglevel))

    #
    # Set debug
    #

    # We don't need logging level, only 'True' or 'False'
    args.debug = (args.debug == logging.DEBUG)

    #
    # Colorize log messages, if we any any loglevel equal or below debug level
    #
    if loglevel_min <= logging.DEBUG:
        try:
            import colorlog
        except ImportError:
            pass
        else:
            # Create color formatter
            # Would be so much easier, if this PR were accepted:
            # https://github.com/borntyping/python-colorlog/pull/99
            formatter = colorlog.ColoredFormatter(
                '%(asctime)s '
                '%(log_color)s%(levelname)-8s%(reset)s '
                '%(bold)s%(name)s%(reset)s: '
                '%(message_log_color)s%(message)s%(reset)s',
                datefmt='%H:%M:%S',
                log_colors={
                    'DEBUG':    'cyan',
                    'INFO':     'green',
                    'WARNING':  'yellow',
                    'ERROR':    'red',
                    'CRITICAL': 'bold_red'},
                secondary_log_colors={
                    'message': {
                        'ERROR':    'red',
                        'CRITICAL': 'bold_red'}})
            # Replace formatters of all stream handlers
            for handler in logging.getLogger().handlers:
                if isinstance(handler, logging.StreamHandler):
                    handler.setFormatter(formatter)

    #
    # Start asyncio loop
    #

    # Log start up info
    logging.info(
        f'Connect to mopidy on {args.host}:{args.port}')
    _attempts = ('forever'
                 if args.reconnect_attempts is None
                 else f'{args.reconnect_attempts} times')
    logging.info(
        f'If connection fails or breaks, '
        f'try to (re)connect {_attempts} '
        f'with {args.reconnect_timeout}s between retries')
    logging.info(
        f'Load additional DBus interfaces: '
        f'{", ".join(args.interfaces) or None}')

    # Convert args to a dictionary, so that we can use **kwargs
    kwargs = vars(args)

    while True:
        try:
            # Start either aiorun or asyncio event loop
            try:
                aiorun
            except NameError:
                # Run with standard asyncio event loop
                try:
                    loop = asyncio.get_event_loop()
                    loop.run_until_complete(
                        main_loop(loop_type='asyncio', **kwargs))
                except asyncio.CancelledError:
                    pass
            else:
                # Run forever with aiorun (stop only in debugging mode)
                aiorun.run(
                    main_loop(loop_type='aiorun', **kwargs),
                    stop_on_unhandled_errors=(args.debug))
            break
        except OSError:
            # Network connection error?
            import time
            time.sleep(30)
