"""The Playlists MPRIS D-Bus interface for a remote Mopidy instance.

The D-Bus name of this interface is 'org.mpris.MediaPlayer2.Playlists'.


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

from dbus_next.service import method, dbus_property, PropertyAccess, signal

from .base import _MopidyBaseInterface


logger = logging.getLogger(__name__)


class MopidyPlaylistsInterface(_MopidyBaseInterface):
    """The "org.mpris.MediaPlayer2.Playlists" interface.

    Provides access to the media player's playlists.

    Since D-Bus does not provide an easy way to check for what interfaces are
    exported on an object, clients should attempt to get one of the properties
    on this interface to see if it is implemented.

    See:
        https://specifications.freedesktop.org/mpris-spec/2.2/Playlists_Interface.html
    """

    def __init__(self, mopidy, *args, **kwargs):
        """Initialize the 'MopidyPlaylistsInterface' class.

        Parameters
        ----------
        mopdiy : mopidy_asyncio_client.MopidyClient
            The mopidy client
        *args : arguments
            Passed on to parent class.
        **kwargs : keyword arguments
            Passed on to parent class.

        Returns
        -------
        None.

        """
        super().__init__('org.mpris.MediaPlayer2.Playlists',
                         mopidy, *args, **kwargs)

    #
    # Mopidy events
    #

    async def on_mopidyevent_playlist_changed(self, data):
        """Is called whenever a playlist is changed.

        Parameters
        ----------
        data['playlist'] : mopidy.models.Playlist
            The changed playlist.

        Returns
        -------
        None.

        """
        logger.info(
            'Mopidy event org.mpris.MediaPlayer2.Playlists.playlist_changed'
            '(data=%s) received',
            data)
        self.PlaylistChanged(data['playlist'])

    async def on_mopidyevent_playlist_deleted(self, data):
        """Is called whenever a playlist is deleted.

        Parameters
        ----------
        data['uri'] : str
            The changed playlist.

        Returns
        -------
        None.

        """
        logger.info(
            'Mopidy event org.mpris.MediaPlayer2.Playlists.mute_deleted'
            '(data=%s) received',
            data)
        count = await self._get_PlaylistCount()
        self.emit_properties_changed(
            PlaylistCount=count)

    async def on_mopidyevent_playlists_loaded(self, data):
        """Is called whenever a playlist is loaded or refreshed.

        Parameters
        ----------
        data : {}
            No data supplied, hence an empty dictionary.

        Returns
        -------
        None.

        """
        logger.info(
            'Mopidy event org.mpris.MediaPlayer2.Playlists.mute_loaded'
            '(data=%s) received',
            data)
        count = await self._get_PlaylistCount()
        self.emit_properties_changed(
            PlaylistCount=count)

    #
    # Methods
    #

    # ActivatePlaylist(o: PlaylistId)                   → nothing

    @method()
    async def ActivatePlaylist(self, playlist_id: 'o'):
        """Start playing the given playlist.

        This must be implemented! If the media player does not allow clients
        to change the playlist, it should not implement this interface at all.

        It is up to the media player whether this completely replaces the
        current tracklist, or whether it is merely inserted into the tracklist
        and the first track starts. For example, if the media player is
        operating in a "jukebox" mode, it may just append the playlist to the
        list of upcoming tracks, and skip to the first track in the playlist.

        Parameters
        ----------
        playlist_id : PlaylistId
            The id of the playlist to activate.

        Returns
        -------
        None.

        """
        logger.info(
            'Method org.mpris.MediaPlayer2.Playlists.ActivatePlaylist'
            '(playlist_id=%s) called',
            playlist_id)
        playlist_uri = self.dbusid_to_playlistid(playlist_id)
        playlist = await self.mopidy.playlists.lookup(playlist_uri)
        if playlist and playlist.tracks:
            tl_tracks = await self.mopidy.tracklist.add(playlist.tracks)
            await self.player.play(tlid=tl_tracks[0].tlid)

    # GetPlaylists(u: Index, u: MaxCount, s: Order, b: ReverseOrder)
    #                                                   → a(oss): Playlists

    @method()
    async def GetPlaylists(self,
                           index: 'u', max_count: 'u',
                           order: 's', reverse_order: 'b') -> 'a(oss)':
        """Get a set of playlists.

        Parameters
        ----------
        index : int
            The index of the first playlist to be fetched (according to the
            ordering).
        max_count : int
            The maximum number of playlists to fetch.
        order : PlaylistOrdering
            The ordering that should be used.
        reverse_order : bool
            'False':
                The order is not reversed.
            'True':
                The order should be reversed.

        Returns
        -------
        [PlayList]
            A list of (at most 'max_count') playlists.

        """
        logger.info(
            'Method org.mpris.MediaPlayer2.Playlists.GetPlaylists'
            '(index=%s, max_count=%s, order=%s, reverse_order=%s) called',
            index, max_count, order, reverse_order)
        # Get playlists
        playlists = await self.mopidy.playlists.as_list()
        # Order playlists
        if order == 'Alphabetical':
            # Order by playlist.name
            playlists.sort(key=lambda p: p.name, reverse=reverse_order)
        elif order == 'User':
            # Do not change order
            if reverse_order:
                playlists.reverse()
            else:
                pass
        # Return requested slice
        return [(self.playlist_to_dbusid(playlists), playlists.name, '')
                for playlist in playlists[index:index+max_count]]

    #
    # Signals
    #

    # PlaylistChanged((oss): Playlist)

    @signal()
    def PlaylistChanged(self, playlist: '(oss)') -> '(oss)':
        """Indicate that 'Name' or 'Icon' attribute of a playlist has changed.

        Indicates that either the 'Name' or 'Icon' attribute of a playlist has
        changed.

        Client implementations should be aware that this signal may not be
        implemented.

        Parameters
        ----------
        playlist : PlayList
            The playlist which details have changed.

        Returns
        -------
        PlayList
            The playlist which details have changed.

        """
        logger.info(
            'Signal org.mpris.MediaPlayer2.Playlists.PlaylistChanged'
            '(playlist=%s) to emit',
            playlist)
        return playlist

    #
    # Properties
    #

    # PlaylistCount         u                       Read only

    @dbus_property(access=PropertyAccess.READ)
    async def PlaylistCount(self) -> 'u':                       # noqa: D401
        """The number of playlists available.

        Signals
        ----------
        org.freedesktop.DBus.Properties.PropertiesChanged
            This signal is emitted with the new value every time this
            property changes.

        Returns
        -------
        int
            The number of playlists available.

        """
        logger.info(
            'Property org.mpris.MediaPlayer2.Playlists.PlaylistCount '
            'requested')
        return await self._get_PlaylistCount()

    async def _get_PlaylistCount(self):
        playlists = await self.mopidy.playlists.as_list()
        return len(playlists)

    # Orderings             as (Playlist_Ordering_List)     Read only

    @dbus_property(access=PropertyAccess.READ)
    def Orderings(self) -> 'as':                                # noqa: D401
        """The available orderings.

        Signals
        -------
        org.freedesktop.DBus.Properties.PropertiesChanged
            This signal is emitted with the new value every time this
            property changes.

        Returns
        -------
        [PlaylistOrdering]
            The available orderings. At least one must be offered.

        """
        logger.info(
            'Property org.mpris.MediaPlayer2.Playlists.Orderings '
            'requested')
        return self._get_Orderings()

    def _get_Orderings(self):
        # Hard coded as in 'mopidy_mpris/playlists.py'
        return [
            "Alphabetical",     # Order by playlist.name
            "User"]             # Don't change order

    # ActivePlaylist        (b(oss)) (Maybe_Playlist)       Read only

    @dbus_property(access=PropertyAccess.READ)
    def ActivePlaylist(self) -> '(b(oss))':               # noqa: D401
        """The currently-active playlist.

        Note that this may not have a value even after 'ActivatePlaylist()'
        is called with a valid playlist id as 'ActivatePlaylist()'
        implementations have the option of simply inserting the contents of
        the playlist into the current tracklist.

        Signals
        -------
        org.freedesktop.DBus.Properties.PropertiesChanged
            This signal is emitted with the new value every time this
            property changes.

        Returns
        -------
        [MaybePlaylist]
            List of 'MaybePlaylist' items.

            If there is no currently-active playlist, the structure's 'valid'
            field will be 'False', and the 'Playlist' details are undefined.

        """
        logger.info(
            'Property org.mpris.MediaPlayer2.Playlists.ActivePlaylist '
            'requested')
        return self._get_ActivePlaylist()

    def _get_ActivePlaylist(self):
        # Hard coded as in 'mopidy_mpris/playlists.py'
        return [False, ['/', 'None', '']]
