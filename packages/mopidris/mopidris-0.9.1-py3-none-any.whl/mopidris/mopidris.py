"""MPRIS D-Bus for a remote Mopidy instance.

Control a remote Mopidy instance through DBus, e.g. with sound applets.

Many desktop environments can control a media player through the
D-Bus (http://www.freedesktop.org/wiki/Software/dbus) via the
Media Player Remote Interfacing Specification (MPRIS)
(https://specifications.freedesktop.org/mpris-spec/latest/) interface. To
control a locally running instance of Mopidy, there exists the `Mopidy-MPRIS`
package:
- https://mopidy.com/ext/mpris/
- https://pypi.org/project/Mopidy-MPRIS
- https://github.com/mopidy/mopidy-mpris

For this to work, Mopidy has to run on the same computer as the the D-Bus. If
Mopidy runs on a remote server, there was only the following solution
available:
1. Install and enable the MPD interface for Mopidy:
    - https://mopidy.com/ext/mpd/
    - https://pypi.org/project/Mopidy-MPD/
    - https://github.com/mopidy/mopidy-mpd
2. Install [`mpDris2`](https://github.com/eonpatapon/mpDris2).
3. Start `mpDris2`, whenever you log into your desktop environment.

`mopidris` connects directly to the remote Mopidy without the detour through
the `mpd` interface.


Optional packages
=================

You can install the following optional packages. `mopidris` makes use of them,
if it can find them, but it also works well without them:
1. `aiorun`: If the event loop is terminated with CTRL-C, sometimes the port
   is not released and 'mopidris' cannot be restarted. 'aiorun' can help here
   (but it can still happen, that the DBUS hangs ...)
    - https://pypi.org/project/aiorun/
    - https://github.com/cjrh/aiorun
2. `colored_traceback`: Shows coloured tracebacks, to help debugging
   exceptions.
    - https://pypi.org/project/colored-traceback
    - https://github.com/staticshock/colored-traceback.py
3. `colorlog`: Colour the log to make it easier to read.
    - https://pypi.org/project/colorlog/
    - https://github.com/borntyping/python-colorlog


Usage
=====

'__main__.py' contains the logic for being called from a command line, so this
package can be called as `python3 mopidris`. For more information see
`python3 mopidris --help`, '__main__.py' and the README file.


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

import logging

import dbus_next as dbus
from mopidy_asyncio_client import MopidyClient


logger = logging.getLogger(__name__)


async def main_loop(host=None, port=None,
                    interfaces=[],
                    can_quit=False,
                    mangle=True,
                    loop_type='asyncio',
                    debug=False,
                    **kwargs):
    """Asyncio's main loop function.

    Parameters
    ----------
    host : str, optional
        The host or ip address, where the Mopidy instance can be found.
        The default is 'None', using 'mopidy_asyncio_client.MopidyClient''s
        default host ("localhost").
    port : int, optional
        The port number, where the Mopidy instance can be found.
        The default is 'None', using 'mopidy_asyncio_client.MopidyClient''s
        default port number (6680).
    interfaces : [str]
        A list with the additional interfaces to be activated. Valid values
        "tracklist" and "playlists".
    loop_type : str, optional
        The type of the loop. Currently supported are "aiorun" and the
        standard "asyncio".
        The default is "asyncio".
    can_quit : bool
        If the program advertise, that it can be quit.
    mangle : bool
        If the titles of Internet radio streams should be split at " - " into
        artist and title.
    debug : bool, optional
        If debug output should be generated.
        The default is 'False'.self._decoder = None
    **kwargs
        Further keyword arguments passed on to 'MopidyClient()'.

    Returns
    -------
    None.

    """
    # We could have incorporated these keywords into '**kwargs', but we want
    # to have them stand out...
    if host is not None:
        kwargs['host'] = host
    if port is not None:
        kwargs['port'] = port

    bus_name = f"RemoteMopidy._{host.replace('.', '_')}__{port}"

    async with MopidyClient(**kwargs) as mopidy:

        logger.info('%r', mopidy)

        #
        # DBus message bus
        #

        bus = await dbus.aio.MessageBus().connect()
        logger.debug('%r', bus)

        #
        # DBus Interfaces
        #
        # Only import interfaces, which were specified

        # Import and initiate them
        from interfaces.root import MopidyInterface
        root_interface = MopidyInterface(
            mopidy, can_quit=can_quit, loop_type=loop_type)

        from interfaces.player import MopidyPlayerInterface
        player_interface = MopidyPlayerInterface(
            mopidy, mangle=mangle)

        if 'tracklist' in interfaces:
            from interfaces.tracklist import MopidyTrackListInterface
            tracklist_interface = MopidyTrackListInterface(
                mopidy, player_interface)

        if 'playlists' in interfaces:
            from interfaces.playlists import MopidyPlaylistsInterface
            playlists_interface = MopidyPlaylistsInterface(
                mopidy)

        # Make them available on the DBUS
        bus.export('/org/mpris/MediaPlayer2', root_interface)
        bus.export('/org/mpris/MediaPlayer2', player_interface)
        if 'tracklist' in interfaces:
            bus.export('/org/mpris/MediaPlayer2', tracklist_interface)
        if 'playlists' in interfaces:
            bus.export('/org/mpris/MediaPlayer2', playlists_interface)

        await bus.request_name(f'org.mpris.MediaPlayer2.{bus_name}')

        #
        # Bind Mopidy events to the the org.mpris.MediaPlayer2 interfaces.
        #
        # Available Mopidy events are described in:
        #   https://docs.mopidy.com/en/latest/api/core/#core-events
        #

        # Catch all
        if debug:
            # Mopidy's catch all 'on_event(event, **kwargs)' is exposed as
            # '*' in 'mopidy_asyncio_client'; only catch it, if we are in debug
            # mode - and do it first, so that we get the event displayed
            # before it is processed by the special event listeners
            mopidy.bind('*', root_interface._debug_event)

        # Bind events for org.mpris.MediaPlayer2 interface; yes, there are none
        for event in ():
            mopidy.bind(
                event,
                getattr(root_interface, f'on_mopidyevent_{event}'))

        # Bind events for org.mpris.MediaPlayer2.Player interface
        for event in ('mute_changed',
                      'options_changed',
                      'playback_state_changed', 'stream_title_changed',
                      'seeked',
                      'volume_changed'):
            mopidy.bind(
                event,
                getattr(player_interface, f'on_mopidyevent_{event}'))

        # Bind events for org.mpris.MediaPlayer2.TrackLists interface
        if 'tracklist' in interfaces:
            for event in ('track_playback_ended', 'track_playback_paused',
                          'track_playback_resumed', 'track_playback_started',
                          'tracklist_changed'):
                mopidy.bind(
                    event,
                    getattr(tracklist_interface, f'on_mopidyevent_{event}'))

        # Bind events for org.mpris.MediaPlayer2.Playlists interface
        if 'playlists' in interfaces:
            for event in ('playlist_changed', 'playlist_deleted',
                          'playlists_loaded'):
                mopidy.bind(
                    event,
                    getattr(playlists_interface, f'on_mopidyevent_{event}'))

        await bus.wait_for_disconnect()
