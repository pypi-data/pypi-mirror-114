"""A base MPRIS D-Bus interface for a remote Mopidy instance.

Control a remote Mopidy instance through D-Bus, e.g. with sound applets.

MPRIS D-Bus Interface Specification
===================================

The Media Player Remote Interfacing Specification is a standard D-Bus
interface which aims to provide a common programmatic API for controlling
media players.

It provides a mechanism for discovery, querying and basic playback control of
compliant media players, as well as a tracklist interface which is used to add
context to the active media item.

https://specifications.freedesktop.org/mpris-spec/latest/


Bus Name Policy
---------------

Each media player must request a unique bus name which begins with
"org.mpris.MediaPlayer2.". For example:
    - "org.mpris.MediaPlayer2.audacious"
    - "org.mpris.MediaPlayer2.vlc"
    - "org.mpris.MediaPlayer2.bmp"
    - "org.mpris.MediaPlayer2.xmms2"

This allows clients to list available media players (either already running or
which can be started via D-Bus activation)

In the case where the media player allows multiple instances running
simultaneously, each additional instance should request a unique bus name,
adding a dot and a unique identifier to its usual bus name, such as one based
on a UNIX process id. For example, this could be:
    - "org.mpris.MediaPlayer2.vlc.instance7389"

Note: According to the D-Bus specification, the unique identifier "must only
contain the ASCII characters '[A-Z][a-z][0-9]_-'" and "must not begin with a
digit".


Types
-----

Track_Id (object path) - Unique track identifier:

    If the media player implements the 'TrackList' interface and allows the
    same track to appear multiple times in the tracklist, this must be unique
    within the scope of the tracklist.

    Note that this should be a valid D-Bus object id, although clients should
    not assume that any object is actually exported with any interfaces at
    that path.

    Media players may not use any paths starting with "/org/mpris" unless
    explicitly allowed by this specification. Such paths are intended to have
    special meaning, such as "/org/mpris/MediaPlayer2/TrackList/NoTrack" to
    indicate "no track".

MetaData ({str: variant}):

    A mapping from metadata attribute names to values.

    Items:
        key (str):
            The name of the attribute; see the metadata page for guidelines
            on names to use.
        value (variant):
            The value of the attribute, in the most appropriate format.

    Notable keys:
        "mpris:trackid":
            Must always be present!

            Must be of D-Bus type "o". This contains a D-Bus path that
            uniquely identifies the track within the scope of the playlist.
            There may or may not be an actual D-Bus object at that path; this
            specification says nothing about what interfaces such an object
            may implement.
        "mpris:length":
            If the length of the track is known, it should be provided in this
            key. The length must be given in microseconds, and be represented
            as a signed 64-bit integer.
        "mpris:artUrl":
            If there is an image associated with the track, a URL for it may
            be provided using this key.
        "xesam:...":
            For other metadata, fields defined by the Xesam ontology
            (http://xesam.org/main/XesamOntology) should be used, prefixed by
            "xesam:". See the metadata page on the freedesktop.org wiki
            (http://www.freedesktop.org/wiki/Specifications/mpris-spec/metadata)
            for a list of common fields.

PlaylistId (str):

    Unique playlist identifier.

    This is a D-Bus object id as that is the definitive way to have unique
    identifiers on D-Bus. It also allows for future optional expansions to the
    specification where tracks are exported to D-Bus with an interface similar
    to "org.gnome.UPnP.MediaItem2".

PlayList ([[id, name, icon]]):

    A 'list' describing a playlist.

    Items:
        id (PlaylistId):
            A unique identifier for the playlist.

            This should remain the same if the playlist is renamed.
        name (str):
            The name of the playlist, typically given by the user.
        icon (str):
            The URI of an (optional) icon.

MaybePlaylist ([valid, playlist]):

    A data structure describing a playlist, or nothing.

    Items:
        valid (bool):
            Whether this structure refers to a valid playlist.
        playlist (PlayList):
            The playlist, providing 'valid' is 'True', otherwise undefined.

            When constructing this type, it should be noted that the playlist
            ID must be a valid object path, or D-Bus implementations may
            reject it. This is true even when 'valid' is 'False'. It is
            suggested that "/" is used as the playlist ID in this case.

PlaylistOrdering (str):

    Specifies the ordering of playlist.

    Values:
        "Alphabetical" (Alphabetical):
            Alphabetical ordering by name, ascending.
        "CreationDate" (Created):
            Ordering by creation date, oldest first.
        "ModifiedDate" (Modified):
            Ordering by last modified date, oldest first.
        "LastPlayDate" (Played):
            Ordering by date of last playback, oldest first.
        "UserDefined" (User):
            A user-defined ordering.


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


logger = logging.getLogger(__name__)


class _MopidyBaseInterface(dbus.service.ServiceInterface):
    """Base class for all "org.mpris.MediaPlayer2" interfaces."""

    _dbusstub_track = '/com/mopidy/track/'
    _dbusstub_playlist = '/com/mopidy/playlist/'

    def __init__(self, interface_name, mopidy):
        """Initialize the '_MopidyInterface' class.

        Parameters
        ----------
        interface_name : str
            The name of the this interface as it appears to clients. Must be
            a valid interface name.
        mopdiy : mopidy_asyncio_client.MopidyClient
            The mopidy client

        Returns
        -------
        None.

        """
        super().__init__(interface_name)
        self.mopidy = mopidy

    async def _debug_event(self, *args, **kwargs):
        """Catch all events from 'mopidy_asyncio_client.MopidyClient'."""
        logger.debug('************ Event ************\n%s', args)

    def emit_properties_changed(self, **changed_properties):
        """Overload the 'emit_properties_changed()' method.

        The 'dbus.service.ServiceInterface.emit_properties_changed()' is
        overloaded
        1. so that this method logs automatically.
        2. and that keyword arguments are used instead of a dictionary


        Parameters
        ----------
        **changed_properties : keyword arguments
            Passed on to overwritten 'emit_properties_changed()'.

        Returns
        -------
        None.

        """
        logger.info(
            'Signal org.freedesktop.DBus.Properties.PropertiesChanged'
            '(%s) to emit',
            changed_properties)
        super().emit_properties_changed(changed_properties)

    def mopidyid_to_dbusid(self, tl_id):
        """Generate the full D-Bus track id from Mopidy's track id.

        Parameters
        ----------
        tl_id : int
            The Mopidy track id.

        Returns
        -------
        str
            The full D-Bus track id.

        """
        return self._dbusstub_track + str(tl_id)

    def tltrack_to_dbusid(self, tl_track):
        """Generate the full D-Bus track id from Mopidy's 'tl_track'.

        Parameters
        ----------
        tl_track : mopidy.TlTrack
            A dictionary with track information.

        Returns
        -------
        str
            The full D-Bus track id.

        """
        return self._dbusstub_track + str(tl_track["tlid"])

    def dbusid_to_mopidyid(self, tlid):
        """Convert a D-Bus track id to Mopidy's tl_id.

        Parameters
        ----------
        tlid : str
            A string starting with the D-Bus path '/com/mopidy/track/'.

        Raises
        ------
        ValueError:
            If the 'tlid' does not start with '/com/mopidy/track' or the id
            cannot be converted to in integer value.

        Returns
        -------
        int
            The Mopidy tracklist id.

        """
        if tlid.startswith(self._dbusstub_track):
            try:
                return int(tlid.replace(self._dbusstub_track))
            except ValueError as e:
                raise ValueError(
                    f'Could not convert the id to an integer. {e}')
        else:
            raise ValueError(
                f"The id does not start with '{self._dbusstub_track}'. "
                f'Got: {tlid}')

    def playlist_to_dbusid(self, playlist):
        """Generate the full D-Bus playlist id from Mopidy's 'playlist'.

        Parameters
        ----------
        playlist : mopidy.models.Ref
            The playlist.

        Returns
        -------
        str
            The full D-Bus playlist id.

        """
        return self._dbusstub_playlist + str(playlist.uri)

    def dbusid_to_playlistid(self, playlist_id):
        """Convert a D-Bus playlist id to Mopidy's playlist.

        Parameters
        ----------
        playlist_id : str
            A string starting with the D-Bus path '/com/mopidy/playlist/'.

        Raises
        ------
        ValueError
            If the 'playlist_id' does not start with '/com/mopidy/playlist/'.

        Returns
        -------
        str
            The Mopidy playlist id.

        """
        if playlist_id.startswith(self._dbusstub_playlist):
            return playlist_id.replace(self._dbusstub_playlist)
        else:
            raise ValueError(
                f"The id does not start with '{self._dbusstub_playlist}'. "
                f'Got: {playlist_id}')
