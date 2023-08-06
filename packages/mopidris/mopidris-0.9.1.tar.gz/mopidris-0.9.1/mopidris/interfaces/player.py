"""The Player MPRIS D-Bus interface for a remote Mopidy instance.

The D-Bus name of this interface is 'org.mpris.MediaPlayer2.Player'.


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
from dbus_next.service import method, dbus_property, PropertyAccess, signal

from .base import _MopidyBaseInterface


logger = logging.getLogger(__name__)


class MopidyPlayerInterface(_MopidyBaseInterface):
    """The "org.mpris.MediaPlayer2.Player" interface.

    This interface implements the methods for querying and providing basic
    control over what is currently playing.

    See:
        https://specifications.freedesktop.org/mpris-spec/2.2/Player_Interface.html#Property:Rate
    """

    def __init__(self, mopidy, mangle=True, *args, **kwargs):
        """Initialize the 'MopidyPlayerInterface' class.

        Parameters
        ----------
        mopdiy : mopidy_asyncio_client.MopidyClient
            The mopidy client
        mangle : bool
            If the titles of Internet radio streams should be split at " - "
            into artist and title.
        *args : arguments
            Passed on to parent class.
        **kwargs : keyword arguments
            Passed on to parent class.

        Returns
        -------
        None.

        """
        self._mangle = mangle
        super().__init__('org.mpris.MediaPlayer2.Player',
                         mopidy, *args, **kwargs)

    #
    # Mopidy events
    #

    async def on_mopidyevent_mute_changed(self, data):
        """Is called whenever the mute state is changed.

        Parameters
        ----------
        data['mute'] : boolean
            The new mute state.

        Returns
        -------
        None.

        """
        logger.info(
            'Mopidy event org.mpris.MediaPlayer2.Player.mute_changed'
            '(data=%s) received',
            data)
        if data['mute']:
            volume = await self._get_Volume()
        else:
            volume = 0
        self.emit_properties_changed(
            Volume=volume)

    async def on_mopidyevent_options_changed(self, data):
        """Is called whenever an options is changed.

        Returns
        -------
        None.

        """
        loop = await self._get_LoopStatus()
        shuffle = await self._get_Shuffle()
        can_go_previous = await self._get_CanGoPrevious()
        can_go_next = await self._get_CanGoNext()
        self.emit_properties_changed(
            LoopStatus=loop,
            Shuffle=shuffle,
            CanGoPrevious=can_go_previous,
            CanGoNext=can_go_next)

    async def on_mopidyevent_playback_state_changed(self, data):
        """Is called whenever playback state is changed.

        Parameters
        ----------
        data['old_state'] : string from mopidy.core.PlaybackState field
            The state before the chan.
        data['new_state'] : string from mopidy.core.PlaybackState field
            The state after the change.

        Returns
        -------
        None.

        """
        logger.info(
            'Mopidy event org.mpris.MediaPlayer2.Player.playback_state_changed'
            '(data=%s) received',
            data)
        status = data['new_state']
        self.emit_properties_changed(
            PlaybackStatus=status.capitalize())
        if status == 'playing':
            metadata = await self._get_Metadata()
            self.emit_properties_changed(
                PlaybackStatus=status.capitalize(),
                Metadata=metadata)

    async def on_mopidyevent_stream_title_changed(self, data):
        """Is called whenever the currently playing stream title changes.

        Parameters
        ----------
        data['title'] : string
            The new stream title.

        Returns
        -------
        None.

        """
        logger.info(
            'Mopidy event org.mpris.MediaPlayer2.Player.stream_title_changed'
            '(data=%s) received',
            data)
        metadata = await self._get_Metadata()
        self.emit_properties_changed(
            Metadata=metadata)

    async def on_mopidyevent_seeked(self, data):
        """Is called whenever the time position changes by an unexpected amount.

        E.g. at seek to a new time position.

        Parameters
        ----------
        data['time_position'] : int
            The position that was seeked to in milliseconds.

        Returns
        -------
        None.

        """
        logger.info(
            'Mopidy event org.mpris.MediaPlayer2.Player.seeked'
            '(data=%s) received',
            data)
        # in µs
        self.Seeked(data['time_position'] * 1000)

    async def on_mopidyevent_volume_changed(self, data):
        """Is called whenever the volume is changed.

        Parameters
        ----------
        data ['volume'] : int
             The new volume in the range [0..100].

        Returns
        -------
        None.

        """
        logger.info(
            'Mopidy event org.mpris.MediaPlayer2.Player.volume_changed'
            '(data=%s) received',
            data)
        self.emit_properties_changed(
            Volume=data['volume']/100)

    #
    # Methods
    #

    # Next()                                            → nothing

    @method()
    async def Next(self):
        """Skip to the next track in the tracklist.

        If there is no next track (and endless playback and track repeat are
        both off), stop playback.

        If playback is paused or stopped, it remains that way.

        If 'CanGoNext' is 'False', attempting to call this method should have
        no effect.

        Returns
        -------
        None.

        """
        logger.info(
            'Method org.mpris.MediaPlayer2.Player.Next() called')
        if await self._get_CanGoNext():
            await self.mopidy.playback.next()
        else:
            pass

    # Previous()                                        → nothing

    @method()
    async def Previous(self):
        """Skip to the previous track in the tracklist.

        If there is no previous track (and endless playback and track repeat
        are both off), stop playback.

        If playback is paused or stopped, it remains that way.

        If 'CanGoPrevious' is 'False', attempting to call this method should
        have no effect.

        Returns
        -------
        None.

        """
        logger.info(
            'Method org.mpris.MediaPlayer2.Player.Previous() called')
        if await self._get_CanGoPrevious():
            await self.mopidy.playback.previous()
        else:
            pass

    # Pause()                                           → nothing

    @method()
    async def Pause(self):
        """Pause playback.

        If playback is already paused, this has no effect.

        Calling 'Play()' after this should cause playback to start again from
        the same position.

        If 'CanPause' is 'False', attempting to call this method should have
        no effect

        Returns
        -------
        None.

        """
        logger.info(
            'Method org.mpris.MediaPlayer2.Player.Pause() called')
        if self._get_CanPause():
            await self.mopidy.playback.pause()
        else:
            pass

    # PlayPause()                                       → nothing

    @method()
    async def PlayPause(self):
        """Pause playback.

        If playback is already paused, resumes playback.

        If playback is stopped, starts playback.

        If 'CanPause' is 'False', attempting to call this method should have
        no effect and raise an error.

        Raises
        ------
        NotSupported
            Raised, if the 'CanPause' property is 'False'.

        Returns
        -------
        None.

        """
        logger.info(
            'Method org.mpris.MediaPlayer2.Player.PlayPause() called')
        if self.CanPause:
            state = await self._get_PlaybackStatus()
            if state == 'playing':
                await self.mopidy.playback.pause()
            elif state == 'paused':
                if await self._get_CanPlay():
                    await self.mopidy.playback.resume()
            elif state == 'stopped':
                await self.mopidy.playback.play()
        else:
            dbus.DBusError(
                dbus.ErrorType.NOT_SUPPORTED,
                f'{self.mopidy} cannot pause')

    # Stop()                                            → nothing

    @method()
    async def Stop(self):
        """Stop playback.

        If playback is already stopped, this has no effect.

        Calling 'Play()' after this should cause playback to start again from
        the beginning of the track.

        If 'CanControl' is 'False', attempting to call this method should have
        no effect and raise an error.

        Raises
        ------
        NotSupported
            Raised, if the 'CanControl' property is 'False'.

        Returns
        -------
        None.

        """
        logger.info(
            'Method org.mpris.MediaPlayer2.Player.Stop() called')
        if self._get_CanControl():
            await self.mopidy.playback.stop()
        else:
            dbus.DBusError(
                dbus.ErrorType.NOT_SUPPORTED,
                f'{self.mopidy} cannot stop')

    # Play()                                            → nothing

    @method()
    async def Play(self):
        """Start or resumes playback.

        If already playing, this has no effect.

        If paused, playback resumes from the current position.

        If there is no track to play, this has no effect.

        If 'CanPlay' is 'False', attempting to call this method should have
        no effect.

        Returns
        -------
        None.

        """
        logger.info(
            'Method org.mpris.MediaPlayer2.Player.Play() called')
        if await self._get_CanPlay():
            state = await self._get_PlaybackStatus()
            if state == 'paused':
                await self.mopidy.playback.resume()
            else:
                await self.mopidy.playback.play()
        else:
            pass

    # Seek(x: Offset in µs)                             → nothing

    @method()
    async def Seek(self, offset: 'x'):
        """Seek forward in the current track.

        If the 'CanSeek' property is 'False', this has no effect.

        Parameters
        ----------
        offset : float
            The number of microseconds to seek forward.

            A negative value seeks back. If this would mean seeking back
            further than the start of the track, the position is set to 0.

            If the value passed in would mean seeking beyond the end of the
            track, acts like a call to 'Next()'.

        Returns
        -------
        None.

        """
        logger.info(
            'Method org.mpris.MediaPlayer2.Player.Seek'
            '(offset=%s) called',
            offset)
        if await self._get_CanSeek():
            # in ms
            position = await self._get_Position()
            position += offset // 1000
            position = min(0, position)
            # If position would mean to seek beyond the end of the track,
            # act like a call to Next()
            tl_track = await self.mopidy.playback.get_current_tl_track()
            if position <= tl_track['track']['length']:
                await self.mopidy.playback.seek(position)
            else:
                await self.mopidy.playback.next()
        else:
            pass

    # SetPosition(o: TrackId, x: Position in µs)        → nothing

    @method()
    async def SetPosition(self, track_id: 'o', position: 'x'):
        """Set the current track position.

        If the 'position' argument is less than 0, do nothing.

        If the 'position' argument is greater than the track length,
        do nothing.

        If the 'CanSeek' property is 'False', this has no effect.

        Parameters
        ----------
        track_id : TrackId
            The currently playing track's identifier.

            If this does not match the id of the currently-playing track,
            the call is ignored as "stale".
        position : float (0 ≤ position ≤ <track_length>)
            Track position in microseconds.

        Returns
        -------
        None.

        """
        logger.info(
            'Method org.mpris.MediaPlayer2.Player.SetPosition'
            '(track_id=%s, position=%s) called',
            track_id, position)
        if self.CanSeek:

            if position < 0:
                return

            # in ms
            position //= 1000
            tl_track = await self.mopidy.playback.get_current_tl_track()

            if tl_track is None:
                return
            if track_id != self.tltrack_to_dbusid(tl_track):
                return
            if tl_track.track.length < position:
                return
            await self.mopidy.playback.seek(position)
        else:
            pass

    # OpenUri(s: Uri)                                   → nothing

    @method()
    async def OpenUri(self, uri: 's'):
        """Open the 'uri'.

        If the playback is stopped, starts playing.

        If the uri scheme or the mime-type of the uri to open is not supported,
        this method does nothing and may raise an error. In particular, if the
        list of available uri schemes is empty, this method may not be
        implemented.

        Clients should not assume that the 'uri' has been opened as soon as
        this method returns. They should wait until the "mpris:trackid" field
        in the 'Metadata' property changes.

        If the media player implements the 'TrackList' interface, then the
        opened track should be made part of the tracklist, the
        "org.mpris.MediaPlayer2.TrackList.TrackAdded" or
        "org.mpris.MediaPlayer2.TrackList.TrackListReplaced" signal should be
        fired, as well as the
        "org.freedesktop.DBus.Properties.PropertiesChanged" signal on the
        tracklist interface.

        Parameters
        ----------
        uri : str
            'uri' of the track to load. Its uri scheme should be an element
            of the "org.mpris.MediaPlayer2.SupportedUriSchemes" property and
            the mime-type should match one of the elements of the
            "org.mpris.MediaPlayer2.SupportedMimeTypes".

        Raises
        ------
        NotSupported
            May be raised, if the uri scheme or the mime-type of the uri to
            open is not supported.

        Returns
        -------
        None.

        """
        logger.info(
            'Method org.mpris.MediaPlayer2.Player.OpenUri'
            '(uri=uri) called',
            uri)
        tl_tracks = await self.mopidy.tracklist.add(uris=[uri])
        if tl_tracks:
            await self.mopidy.playback.play(tlid=tl_tracks[0].tlid)
            # dbus.DBusError(
            #     dbus.ErrorType.NOT_SUPPORTED,
            #     f'{self.mopidy} does not support uri {uri}')
            # dbus.DBusError(
            #     dbus.ErrorType.NOT_SUPPORTED,
            #     f'{self.mopidy} cannot mime type {XXX}')

    #
    # Signals
    #

    # Seeked(x: Position)

    @signal()
    def Seeked(self, val: 'x') -> 'x':
        """Indicate that the track position has changed in an inconsistant way.

        Indicates that the track position has changed in a way that is
        inconsistant with the current playing state.

        When this signal is not received, clients should assume that:
            - When playing, the position progresses according to the rate
              property.
            - When paused, it remains constant.

        This signal does not need to be emitted when playback starts or when
        the track changes, unless the track is starting at an unexpected
        position. An expected position would be the last known one when going
        from 'paused' to 'playing', and 0 when going from 'stopped' to
        'playing'.

        Parameters
        ----------
        val : int
            The new position, in microseconds.

        Returns
        -------
        int
            The new position in microseconds.

        """
        logger.info(
            'Signal org.mpris.MediaPlayer2.Seeked() to emit')
        return val

    #
    # Properties
    #

    # PlaybackStatus        s (Playback_Status)     Read only

    @dbus_property(access=PropertyAccess.READ)
    async def PlaybackStatus(self) -> 's':                      # noqa: D401
        """The current playback status.

        Signals
        -------
        org.freedesktop.DBus.Properties.PropertiesChanged
            This signal is emitted with the new value every time this
            property changes.

        Returns
        -------
        str
            "Playing":
                The media player is playing.
            "Paused":
                The media player is paused.
            "Stopped":
                The media player is stopped.

        """
        logger.info(
            'Property org.mpris.MediaPlayer2.Player.PlaybackStatus requested')
        status = await self._get_PlaybackStatus()
        return status.capitalize()

    async def _get_PlaybackStatus(self):
        return await self.mopidy.playback.get_state()

    # LoopStatus            s (Loop_Status)         Read/Write (optional)

    @dbus_property(access=PropertyAccess.READWRITE)
    async def LoopStatus(self) -> 's':                          # noqa: D401
        """The current loop / repeat status.

        Signals
        -------
        org.freedesktop.DBus.Properties.PropertiesChanged
            This signal is emitted with the new value every time this
            property changes.

        Parameters
        ----------
        value : str
            "None":
                The playback will stop when there are no more tracks to play.
            "Track":
                The current track will start again from the begining once it
                has finished playing.
            "Playlist":
                The playback will loop through a list of tracks.

        Returns
        -------
        str
            "None":
                The playback stops when there are no more tracks to play.
            "Track":
                The current track starts again from the begining once it has
                finished playing.
            "Playlist":
                The playback loops through a list of tracks.

        """
        logger.info(
            'Property org.mpris.MediaPlayer2.Player.LoopStatus requested')
        status = await self._get_LoopStatus()
        return str(status).capitalize()

    @LoopStatus.setter
    async def LoopStatus(self, value: 's'):
        logger.info(
            'Property org.mpris.MediaPlayer2.Player.LoopStatus set to: %s',
            value)
        await self._set_LoopStatus(value)

    async def _get_LoopStatus(self):
        repeat = await self.mopidy.tracklist.get_repeat()
        if not repeat:
            return None

        single = await self.mopidy.tracklist.get_single()
        if single:
            return 'track'
        else:
            return 'playlist'

    async def _set_LoopStatus(self, value):
        if self._get_CanControl():
            if value is None:
                await self.mopidy.tracklist.set_repeat(False)
                await self.mopidy.tracklist.set_single(False)
            elif value == 'track':
                await self.mopidy.tracklist.set_repeat(True)
                await self.mopidy.tracklist.set_single(True)
            elif value == 'playlist':
                await self.mopidy.tracklist.set_repeat(True)
                await self.mopidy.tracklist.set_single(False)
            self.emit_properties_changed(
                LoopStatus=str(value).capitalize())
        else:
            pass

    # Rate                  d (Playback_Rate)       Read/Write

    @dbus_property(access=PropertyAccess.READWRITE)
    def Rate(self) -> 'd':                                      # noqa: D401
        """The current playback rate.

        If the media player has no ability to play at speeds other than the
        normal playback rate, this must still be implemented, and must return
        1.0. The 'MinimumRate' and 'MaximumRate' properties must also be set
        to 1.0.

        Not all values may be accepted by the media player. It is left to the
        media player implementations to decide how to deal with values they
        cannot use; they may either ignore them or pick a "best fit" value.
        Clients are recommended to only use sensible fractions or multiples
        of 1 (e.g.: 0.5, 0.25, 1.5, 2.0, etc).

        Signals
        -------
        org.freedesktop.DBus.Properties.PropertiesChanged
            This signal is emitted with the new value every time this
            property changes.

        Parameters
        ----------
        value : float ('MinimumRate' < value < 'MaximumRate', ≠ 0)
            If playback is paused, the 'PlaybackStatus' property should be
            used to indicate this. A value of 0.0 should not be set by the
            client. If it is, the media player should act as though 'Pause()'
            was called.

        Returns
        -------
        float
            The current playback rate.

        """
        logger.info(
            'Property org.mpris.MediaPlayer2.Player.Rate requested')
        return self._get_Rate()

    @Rate.setter
    async def Rate(self, value: 'd'):
        logger.info(
            'Property org.mpris.MediaPlayer2.Player.Rate set to: %s',
            value)
        await self._set_Rate(value)

    def _get_Rate(self):
        return 1.

    async def _set_Rate(self, value):
        if self._get_CanPause() and value == 0:
            await self.mopidy.playback.pause()

    # Shuffle               b                       Read/Write (optional)

    @dbus_property(access=PropertyAccess.READWRITE)
    async def Shuffle(self) -> 'b':                             # noqa: D401
        """Whether the playback is progressing linearly through a playlist.

        Signals
        -------
        org.freedesktop.DBus.Properties.PropertiesChanged
            This signal is emitted with the new value every time this
            property changes.

        Parameters
        ----------
        value : bool
            'False':
                The playback should progress linearly through a playlist.
            'True':
                The playback should progress in some other order.

            If 'CanControl' is 'False', attempting to set this property
            should have no effect and raise an error.

        Raises
        ------
        NotSupported
            Raised, if the 'CanControl' property is 'False'.

        Returns
        -------
        bool
            'False':
                The playback is progressing linearly through a playlist.
            'True':
                The playback is progressing through a playlist in some other
                order.

        """
        logger.info(
            'Property org.mpris.MediaPlayer2.Player.Shuffle requested')
        if self._get_CanControl():
            return await self._get_Shuffle()
        else:
            return False

    @Shuffle.setter
    async def Shuffle(self, value: 'b'):
        logger.info(
            'Property org.mpris.MediaPlayer2.Player.Shuffle set to: %s',
            value)
        await self._set_Shuffle(value)

    async def _get_Shuffle(self):
        return await self.mopidy.tracklist.get_random()

    async def _set_Shuffle(self, value):
        if self._get_CanControl():
            value = bool(value)
            await self.mopidy.tracklist.set_random(value)
            self.emit_properties_changed(
                Shuffle=value)
        else:
            dbus.DBusError(
                dbus.ErrorType.NOT_SUPPORTED,
                f'{self.mopidy} cannot shuffle, '
                f'because mopidy cannot be controlled')

    # Metadata              a{sv} (Metadata_Map)    Read only

    @dbus_property(access=PropertyAccess.READ)
    async def Metadata(self) -> 'a{sv}':                        # noqa: D401
        """The metadata of the current element.

        Signals
        -------
        org.freedesktop.DBus.Properties.PropertiesChanged
            This signal is emitted with the new value every time this
            property changes.

        Returns
        -------
        {str: MetaData}
            The dictionary with the metadata or an empty dictionary.

            If there is a current track, this must have a "mpris:trackid"
            entry (of D-Bus type "o") at the very least, which contains a
            D-Bus path that uniquely identifies this track.

            See the type documentation for common fields:
                https://www.freedesktop.org/wiki/Specifications/mpris-spec/metadata/

        """
        logger.info(
            'Property org.mpris.MediaPlayer2.Player.Metadata requested')
        return await self._get_Metadata()

    async def _get_Metadata(self, tl_track=None):
        data = {}

        if tl_track is None:
            tl_track = await self.mopidy.playback.get_current_tl_track()
            if tl_track is None:
                return data

        track = tl_track['track']

        # Fill metadata dictionary

        full_track_id = self.tltrack_to_dbusid(tl_track)
        data['mpris:trackid'] = dbus.Variant('o', full_track_id)

        if length := track.get('length', None):
            data['mpris:length'] = dbus.Variant('x', length * 1000)

        if uri := track.get('uri', None):
            data['xesam:url'] = dbus.Variant('s', uri)

            images = await self.mopidy.library.get_images([uri])
            if images and images[uri]:
                largest_image = max(
                    images[uri],
                    key=lambda i: (i.width or 0, i.height or 0))
                data['mpris:artUrl'] = dbus.Variant('s', largest_image['uri'])

        stream_title = await self.mopidy.playback.get_stream_title()
        if title := stream_title or track.get('name', None):
            data['xesam:title'] = dbus.Variant('s', title)

        if artists := track.get('artists', None):
            # artists = list(track.artists)
            # artists.sort(key=lambda a: a.name or '')
            # data['xesam:artist'] = dbus.Variant(
            #     'as', [a.name for a in artists if a.name]
            # )
            data['xesam:artist'] = dbus.Variant(
                'as', [a['name'] for a in artists if 'name' in a])

        # Fix for radio streams, which only hava a title and no artist
        if title and artists is None:
            if self._mangle and (
                    uri.startswith('http')
                    or uri.startswith('orfradio:')):
                # Internet station?
                try:
                    artists, title = title.split(' - ', 1)
                except ValueError:
                    artists, title = None, None
            else:
                artists, title = None, None

            if title is not None and artists is not None:
                data['xesam:title'] = dbus.Variant('s', title)
                # Split on '&' and ','
                data['xesam:artist'] = dbus.Variant(
                    'as', [a.strip()
                           for a in artists.replace('&', ',').split(',')])

        if album := track.get('album', None):
            if name := album.get('name', None):
                data['xesam:album'] = dbus.Variant('s', name)

            if artists := album.get('artists', None):
                # artists = list(track.album.artists)
                # artists.sort(key=lambda a: a.name or '')
                # data['xesam:albumArtist'] = dbus.Variant(
                #     'as', [a.name for a in artists if a.name]
                # )
                data['xesam:albumArtist'] = dbus.Variant(
                    'as',
                    [artist['name'] for artist in artists if 'name' in artist])

        if disc_no := track.get('disc_no', None):
            data['xesam:discNumber'] = dbus.Variant('i', disc_no)

        if track_no := track.get('track_no', None):
            data['xesam:trackNumber'] = dbus.Variant('i', track_no)

        return data

    # Volume                d (Volume)              Read/Write

    @dbus_property(access=PropertyAccess.READWRITE)
    async def Volume(self) -> 'd':                              # noqa: D401
        """The volume level.

        Signals
        -------
        org.freedesktop.DBus.Properties.PropertiesChanged
            This signal is emitted with the new value every time this
            property changes.

        Parameters
        ----------
        value : float (0 ≤ value ≤ 1)
            The volume level. If a negative value is passed, the volume
            should be set to 0.0.

            If 'CanControl' is 'False', attempting to set this property
            should have no effect and raise an error.

        Raises
        ------
        NotSupported
            Raised, if the 'CanControl' property is 'False'.


        Returns
        -------
        float (0 ≤ value ≤ 1)
            The volume level.

        """
        logger.info(
            'Property org.mpris.MediaPlayer2.Player.Volume requested')
        if self._get_CanControl():
            return await self._get_Volume()
        else:
            return 0.

    @Volume.setter
    async def Volume(self, value: 'd'):
        logger.info(
            'Property org.mpris.MediaPlayer2.Player.Volume set to: %s',
            value)
        await self._set_Volume(value)

    async def _get_Volume(self):
        mute = await self.mopidy.mixer.get_mute()
        if mute:
            return 0.

        volume = await self.mopidy.mixer.get_volume()
        if volume is None:
            return 0.
        else:
            # Volume between 0 and 1
            return volume / 100.

    async def _set_Volume(self, value):
        if self._get_CanControl():
            # Volume between 0 and 100
            volume = int(max(0, min(1, value)) * 100)
            await self.mopidy.mixer.set_volume(int(volume*100))
            self.emit_properties_changed(
                Volume=volume/100)
            if volume:
                await self.mopidy.mixer.set_mute(False)
        else:
            dbus.DBusError(
                dbus.ErrorType.NOT_SUPPORTED,
                f'{self.mopidy} cannot set volume, '
                f'because mopidy cannot be controlled')

    # Position              x (Time_In_Us)          Read only

    @dbus_property(access=PropertyAccess.READ)
    async def Position(self) -> 'x':                            # noqa: D401
        """The current track position in microseconds.

        If the media player allows it, the current playback position can be
        changed either with the 'SetPosition()' method or the 'Seek()' method
        on this interface. If this is not the case, the 'CanSeek' property is
        'False', and setting this property has no effect and can raise an
        error.

        Changes
        -------
            Do NOT emit the "org.freedesktop.DBus.Properties.PropertiesChanged"
            signal!

        Signals
        -------
        Seeked
            If the playback progresses in a way that is inconstistant with
            the 'Rate' property, the 'Seeked' signal is emitted.

        Raises
        ------
        NotSupported
            May be raised, if the 'CanSeek' property is 'False'.

        Returns
        -------
        int (0 ≤ value ≤ metadata['mpris:length'])
            The current track position in microseconds, between 0 and the
            "mpris:length" metadata entry (see 'Metadata').

        """
        logger.info(
            'Property org.mpris.MediaPlayer2.Player.Position requested')
        if await self._get_CanSeek():
            position = await self._get_Position()       # in ms
            return position * 1000                      # in µs
        else:
            dbus.DBusError(
                dbus.ErrorType.NOT_SUPPORTED,
                f'{self.mopidy} cannot get position, '
                f'because mopidy cannot be seeked')
            return 0

    async def _get_Position(self):
        # in ms
        return await self.mopidy.playback.get_time_position()

    # MinimumRate           d (Playback_Rate)       Read only

    @dbus_property(access=PropertyAccess.READ)
    def MinimumRate(self) -> 'd':                               # noqa: D401
        """The minimum value, which the 'Rate' property can take.

        Clients should not attempt to set the 'Rate' property below this value.

        Note that even if this value is 0.0 or negative, clients should not
        attempt to set the 'Rate' property to 0.0.

        Signals
        -------
        org.freedesktop.DBus.Properties.PropertiesChanged
            This signal is emitted with the new value every time this
            property changes.

        Returns
        -------
        float (value ≤ 1)
            The minimum value, which the 'Rate' property can take.

        """
        logger.info(
            'Property org.mpris.MediaPlayer2.Player.MinimumRate requested')
        return self._get_MinimumRate()

    def _get_MinimumRate(self):
        return 1.

    # MaximumRate           d (Playback_Rate)       Read only

    @dbus_property(access=PropertyAccess.READ)
    def MaximumRate(self) -> 'd':                               # noqa: D401
        """The maximum value, which the 'Rate' property can take.

        Clients should not attempt to set the 'Rate' property above this value.

        Signals
        -------
        org.freedesktop.DBus.Properties.PropertiesChanged
            This signal is emitted with the new value every time this
            property changes.

        Returns
        -------
        float (value ≥ 1)
            The maximum value, which the 'Rate' property can take.

        """
        logger.info(
            'Property org.mpris.MediaPlayer2.Player.MaximumRate requested')
        return self._get_MaximumRate()

    def _get_MaximumRate(self):
        return 1.

    # CanGoNext             b                       Read only

    @dbus_property(access=PropertyAccess.READ)
    async def CanGoNext(self) -> 'b':
        """Whether the client can call the 'Next()' method.

        Signals
        -------
        org.freedesktop.DBus.Properties.PropertiesChanged
            This signal is emitted with the new value every time this
            property changes.

        Returns
        -------
        bool
            'False':
                The client cannot call the 'Next()' method on this interface.
            'True':
                The client can call the 'Next()' method on this interface and
                expect the current track to change.

            If it is unknown, whether a call to 'Next()' will be successful
            (for example, when streaming tracks), this property should be set
            to 'True'.

            If the 'CanControl' property is 'False', this property should
            also be 'False'.

        """
        logger.info(
            'Property org.mpris.MediaPlayer2.Player.CanGoNext requested')
        return await self._get_CanGoNext()

    async def _get_CanGoNext(self):
        if self._get_CanControl():
            current_tlid = await self.mopidy.playback.get_current_tlid()
            next_tlid = await self.mopidy.tracklist.get_next_tlid()
            return current_tlid != next_tlid
        else:
            return False

    # CanGoPrevious         b                       Read only

    @dbus_property(access=PropertyAccess.READ)
    async def CanGoPrevious(self) -> 'b':
        """Whether the client can call the 'Previous()' method.

        Signals
        -------
        org.freedesktop.DBus.Properties.PropertiesChanged
            This signal is emitted with the new value every time this
            property changes.

        Returns
        -------
        bool
            'False':
                The client cannot call the 'Previous()' method on this
                interface.
            'True':
                The client can call the 'Previous()' method on this
                interface and expect the current track to change.

            If it is unknown, whether a call to 'Previous()' will be
            successful (for example, when streaming tracks), this property
            should be set to 'True'.

            If the 'CanControl' property is 'False', this property should
            also be 'False'.

        """
        logger.info(
            'Property org.mpris.MediaPlayer2.Player.CanGoPrevious requested')
        return await self._get_CanGoPrevious()

    async def _get_CanGoPrevious(self):
        if self._get_CanControl():
            current_tlid = await self.mopidy.playback.get_current_tlid()
            prev_tlid = await self.mopidy.tracklist.get_previous_tlid()
            return current_tlid != prev_tlid
        else:
            return False

    # CanPlay               b                       Read only

    @dbus_property(access=PropertyAccess.READ)
    async def CanPlay(self) -> 'b':
        """Whether playback can be started using 'Play()' or 'PlayPause()'.

        Note that this is related to whether there is a "current track": the
        value should not depend on whether the track is currently paused or
        playing. In fact, if a track is currently playing (and 'CanControl' is
        'True'), this should be 'True'.

        Signals
        -------
        org.freedesktop.DBus.Properties.PropertiesChanged
            This signal is emitted with the new value every time this
            property changes.

        Returns
        -------
        bool
            'False':
                The playback can not be started.
            'True':
                The playback can be started using 'Play()' or 'PlayPause()'.

            If 'CanControl' is 'False', this property should also be 'False'.

        """
        logger.info(
            'Property org.mpris.MediaPlayer2.Player.CanPlay requested')
        return await self._get_CanPlay()

    async def _get_CanPlay(self):
        if self.CanControl:
            current_tlid = await self.mopidy.playback.get_current_tlid()
            if current_tlid is not None:
                return True
            next_tlid = await self.mopidy.tracklist.get_next_tlid()
            if next_tlid is not None:
                return True
            return False
        else:
            return False

    # CanPause              b                       Read only

    @dbus_property(access=PropertyAccess.READ)
    def CanPause(self) -> 'b':
        """Whether playback can be paused using 'Pause()' or 'PlayPause()'.

        Note that this is an intrinsic property of the current track: its
        value should not depend on whether the track is currently paused or
        playing. In fact, if playback is currently paused (and 'CanControl' is
        'True'), this should be 'True'.

        Signals
        -------
        org.freedesktop.DBus.Properties.PropertiesChanged
            This signal is emitted with the new value every time this
            property changes.

        Returns
        -------
        bool
            'False':
                The playback cannot be paused.
            'True':
                The playback can be paused using 'Pause()' or 'PlayPause()'.

            If 'CanControl' is 'False', this property should also be 'False'.

        """
        logger.info(
            'Property org.mpris.MediaPlayer2.Player.CanPause requested')
        return self._get_CanPause()

    def _get_CanPause(self):
        if self._get_CanControl():
            return True
        else:
            return False

    # CanSeek               b                       Read only

    @dbus_property(access=PropertyAccess.READ)
    async def CanSeek(self) -> 'b':
        """Whether the client can control the playback position using 'Seek()'
        and 'SetPosition()'.

        This may be different for different tracks.

        Signals
        -------
        org.freedesktop.DBus.Properties.PropertiesChanged
            This signal is emitted with the new value every time this
            property changes.

        Returns
        -------
        bool
            'False':
                The playback position cannot be set.
            'True':
                The playback position can be set using 'Seek()' and
                'SetPosition()'.

            If 'CanControl' is 'False', this property should also be 'False'.

        """
        logger.info(
            'Property org.mpris.MediaPlayer2.Player.CanSeek requested')
        return await self._get_CanSeek()

    async def _get_CanSeek(self):
        if self._get_CanControl():
            # The track information has no information, if the media can be
            # seeked. A workaround is to use the '.length' information
            # (because) non-seekable streams usually do not have a length
            tl_track = await self.mopidy.playback.get_current_tl_track()
            if (tl_track
                and tl_track['track'].get('length', None) is not None
            ):
                return True
            else:
                return False
        else:
            return False

    # CanControl            b                       Read only

    @dbus_property(access=PropertyAccess.READ)
    def CanControl(self) -> 'b':
        """Whether the media player may be controlled over this interface.

        This property is not expected to change, as it describes an intrinsic
        capability of the implementation.

        Changes
        -------
            Do NOT emit the "org.freedesktop.DBus.Properties.PropertiesChanged"
            signal!

        Returns
        -------
        bool
            'False':
                Clients should assume that all properties on this interface
                are read-only (and will raise errors if writing to them is
                attempted), no methods are implemented and all other
                properties starting with "Can" are also 'False'.
            'True':
                The media player may be controlled over this interface.

        """
        logger.info(
            'Property org.mpris.MediaPlayer2.Player.CanControl requested')
        return self._get_CanControl()

    def _get_CanControl(self):
        return True
