"""The TrackList MPRIS D-Bus interface for a remote Mopidy instance.

The D-Bus name of this interface is 'org.mpris.MediaPlayer2.TrackList'.


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


class MopidyTrackListInterface(_MopidyBaseInterface):
    """The "org.mpris.MediaPlayer2.TrackList" interface.

    Provides access to a short list of tracks which were recently played or
    will be played shortly. This is intended to provide context to the
    currently-playing track, rather than giving complete access to the media
    player's playlist.

    Example use cases are the list of tracks from the same album as the
    currently playing song or the Rhythmbox play queue.

    Each track in the tracklist has a unique identifier. The intention is that
    this uniquely identifies the track within the scope of the tracklist. In
    particular, if a media item (a particular music file, say) occurs twice in
    the track list, each occurrence should have a different identifier. If a
    track is removed from the middle of the playlist, it should not affect the
    track ids of any other tracks in the tracklist.

    As a result, the traditional track identifiers of URLs and position in the
    playlist cannot be used. Any scheme which satisfies the uniqueness
    requirements is valid, as clients should not make any assumptions about
    the value of the track id beyond the fact that it is a unique identifier.

    Note that the (memory and processing) burden of implementing the
    'TrackList' interface and maintaining unique track ids for the playlist
    can be mitigated by only exposing a subset of the playlist when it is very
    long (the 20 or so tracks around the currently playing track, for example).
    This is a recommended practice as the tracklist interface is not designed
    to enable browsing through a large list of tracks, but rather to provide
    clients with context about the currently playing track.

    See:
        https://specifications.freedesktop.org/mpris-spec/2.2/Track_List_Interface.html#Property:CanEditTracks
    """

    def __init__(self, mopidy, player_interface, *args, **kwargs):
        """Initialize the 'MopidyTrackListInterface' class.

        Parameters
        ----------
        mopdiy : mopidy_asyncio_client.MopidyClient
            The mopidy client
        player_interface : MopidyPlayerInterface
            The D-Bus "org.mpris.MediaPlayer2.Player" interface.
        *args : arguments
            Passed on to parent class.
        **kwargs : keyword arguments
            Passed on to parent class.

        Returns
        -------
        None.

        """
        self.player_interface = player_interface
        super().__init__('org.mpris.MediaPlayer2.TrackList',
                         mopidy, *args, **kwargs)

    #
    # Mopidy events
    #

    async def on_mopidyevent_track_playback_ended(self, data):
        """Is called whenever playback of a track ends.

        Parameters
        ----------
        data['tl_track'] : mopidy.models.TlTrack
            The track that was played before playback stopped.
        data['time_position'] : int
            The time position in milliseconds.

        Returns
        -------
        None.

        """
        logger.info(
            'Mopidy event '
            'org.mpris.MediaPlayer2.TrackLists.track_playback_ended'
            '(data=%s) received',
            data)
        status = await self.player_interface._get_PlaybackStatus()
        metadata = await self.player_interface._get_Metadata(
            tl_track=data['tl_track'])
        self.player_interface.emit_properties_changed(
            PlaybackStatus=status,
            Metadata=metadata)

    async def on_mopidyevent_track_playback_paused(self, data):
        """Is called whenever playback of a track is paused.

        Parameters
        ----------
        data['tl_track'] : mopidy.models.TlTrack
            The track that was playing when playback paused.
        data['time_position'] : int
            The time position in milliseconds.

        Returns
        -------
        None.

        """
        logger.info(
            'Mopidy event '
            'org.mpris.MediaPlayer2.TrackLists.track_playback_paused'
            '(data=%s) received',
            data)
        self.player_interface.emit_properties_changed(
            PlaybackStatus='Paused')

    async def on_mopidyevent_track_playback_resumed(self, data):
        """Is called whenever playback of a track is resumed.

        Parameters
        ----------
        data['tl_track'] : mopidy.models.TlTrack
            The track that was playing when playback resumed.
        data['time_position'] : int
            The time position in milliseconds.

        Returns
        -------
        None.

        """
        logger.info(
            'Mopidy event '
            'org.mpris.MediaPlayer2.TrackLists.track_playback_resumed'
            '(data=%s) received',
            data)
        self.player_interface.emit_properties_changed(
            PlaybackStatus='Playing')

    async def on_mopidyevent_track_playback_started(self, data):
        """Is called whenever a new track starts playing.

        Parameters
        ----------
        data['tl_track'] : mopidy.models.TlTrack
            The track that just started playing.

        Returns
        -------
        None.

        """
        logger.info(
            'Mopidy event '
            'org.mpris.MediaPlayer2.TrackLists.track_playback_started'
            '(data=%s) received',
            data)
        metadata = await self.player_interface._get_Metadata(
            tl_track=data['tl_track'])
        self.player_interface.emit_properties_changed(
            PlaybackStatus='Playing',
            Metadata=metadata)

    async def on_mopidyevent_tracklist_changed(self, data):
        """Is called whenever the tracklist is changed.

        Parameters
        ----------
        data : {}
            No data supplied, hence an empty dictionary.

        Returns
        -------
        None.

        """
        logger.info(
            'Mopidy event org.mpris.MediaPlayer2.TrackLists.tracklist_changed'
            '(data=%s) received',
            data)
        # Nothing to do here
        pass

    #
    # Methods
    #

    # GetTracksMetadata(ao: TrackIds)                   → aa{sv}: Metadata
    @method()
    async def GetTracksMetadata(self, track_ids: 'ao') -> 'aa{sv}':
        """Get all the metadata available for a set of tracks.

        Each set of metadata must have a "mpris:trackid" entry at the very
        least, which contains a string that uniquely identifies this track
        within the scope of the tracklist.

        Parameters
        ----------
        [track_ids]
            The list of track ids for which the metadata is requested.

        Returns
        -------
        [{str: MetaData}]
            List with the metadata of the tracks given as input.

        """
        logger.info(
            'Method '
            'org.mpris.MediaPlayer2.TrackList.GetTracksMetadata(track_ids=%s) '
            'called',
            track_ids)
        # Get list of mopidy ids
        track_ids = [self.dbusid_to_mopidyid(track_id)
                     for track_id in track_ids]
        # Get list of available tracks
        tl_tracks = await self.mopidy.tracklist.get_tl_tracks()
        # Convert list of available tracks to a dictionary
        tl_tracks = {tl_track['tlid']: tl_track
                     for tl_track in tl_tracks
                     if tl_track['tlid'] in track_ids}

        metadata = []
        for track_id in track_ids:
            md = await self.player_interface._get_Metadata(
                tl_track=tl_tracks[track_id])
            metadata.append(md)

        return metadata

    # AddTrack(s: Uri, o: AfterTrack, b: SetAsCurrent)  → nothing

    @method()
    async def AddTrack(self, uri: 's', after_track: 'o', set_as_current: 'b'):
        """Add a 'uri' in the 'TrackList'.

        Clients should not assume that the track has been added at the time
        when this method returns. They should wait for a 'TrackAdded' (or
        'TrackListReplaced') signal.

        If the 'CanEditTracks()' property is 'False', this has no effect.

        Parameters
        ----------
        uri : str
            The URI of the item to add. Its uri scheme should be an element
            of the "org.mpris.MediaPlayer2.SupportedUriSchemes" property and
            the mime-type should match one of the elements of the
            "org.mpris.MediaPlayer2.SupportedMimeTypes".
        after_track : TrackId
            The identifier of the track after which the new item should be
            inserted. The path "/org/mpris/MediaPlayer2/TrackList/NoTrack"
            indicates that the track should be inserted at the start of the
            track list.
        set_as_current : bool
            Whether the newly inserted track should be considered as the
            current track. Setting this to 'True' has the same effect as
            calling 'GoTo()' afterwards.

        Raises
        ------
        NotSupported
            May be raised, if the 'CanEditTracks' property is 'False'.

        Returns
        -------
        None.

        """
        logger.info(
            'Method org.mpris.MediaPlayer2.TrackList.AddTrack'
            '(uri=%s, after_track=%s, set_as_current=%s) called',
            uri, after_track, set_as_current)
        if self._get_CanEditTracks():
            # TODO: Check if the uri is in 'SupportedUriSchemes' and the mime
            # type is in 'SupportedMimeTypes'
            if after_track == '/org/mpris/MediaPlayer2/TrackList/NoTrack':
                at = None
            else:
                # Mopidy id
                after_track = self.dbusid_to_mopidyid(after_track)
                at = await self.mopidy.tracklist.index(tlid=after_track) + 1
            await self.mopidy.tracklist.add(uris=[uri], at_position=at)
            await self.mopidy.playback.play(tlid=at)
            metadata = await self.player_interface._get_metadata()
            self.TrackAdded(metadata, after_track)
        else:
            dbus.DBusError(
                dbus.ErrorType.NOT_SUPPORTED,
                f'{self.mopidy} cannot add a track, '
                f'because mopidy cannot edit the tracklist')

    # RemoveTrack(o: TrackId)                           → nothing

    @method()
    async def RemoveTrack(self, track_id: 'o'):
        """Remove an item from the 'TrackList'.

        Clients should not assume that the track has been removed at the
        time when this method returns. They should wait for a 'TrackRemoved'
        (or 'TrackListReplaced') signal.

        If the track is not part of this tracklist, this has no effect.

        If the 'CanEditTracks' property is 'False', this has no effect.

        Parameters
        ----------
        track_id : TrackId
            Identifier of the track to be removed.

            "/org/mpris/MediaPlayer2/TrackList/NoTrack" is not a valid value
            for this argument.

        Raises
        ------
        NotSupported
            May be raised, if the 'CanEditTracks' property is 'False'.

        Returns
        -------
        None.

        """
        logger.info(
            'Method org.mpris.MediaPlayer2.TrackList.RemoveTrack'
            '(track_id=%s) called',
            track_id)
        if self._get_CanEditTracks():
            # Mopidy id
            tl_id = self.dbusid_to_mopidyid(track_id)
            await self.mopidy.tracklist.remove({'tlid': [tl_id]})
            self.TrackRemoved(track_id)
        else:
            dbus.DBusError(
                dbus.ErrorType.NOT_SUPPORTED,
                f'{self.mopidy} cannot remove a track, '
                f'because mopidy cannot edit the tracklist')

    # GoTo(o: TrackId)                                  → nothing

    @method()
    async def GoTo(self, track_id: 'o'):
        """Skip to the specified 'track_id'.

        If the track is not part of this tracklist, this has no effect.

        If this object is not "/org/mpris/MediaPlayer2", the current
        'TrackList''s tracks should be replaced with the contents of this
        'TrackList', and the 'TrackListReplaced' signal should be fired from
        "/org/mpris/MediaPlayer2".

        Signals
        -------
        org.mpris.MediaPlayer2.TrackListReplaced
            Emit, if the current TrackList's tracks were replaced.

        Parameters
        ----------
        track_id : TrackId
            Identifier of the track to skip to.

            "/org/mpris/MediaPlayer2/TrackList/NoTrack" is not a valid value
            for this argument.

        Returns
        -------
        None.

        """
        logger.info(
            'Method org.mpris.MediaPlayer2.TrackList.GoTo'
            '(track_id=%s) called',
            track_id)
        tracks = await self._get_Tracks()
        # Mopidy id
        tl_id = self.dbusid_to_mopidyid(track_id)
        if track_id in tracks:
            await self.mopidy.playback.play(tlid=tl_id)
            self.TrackListReplaced(tracks, track_id)
        else:
            pass

    #
    # Signals
    #

    # TrackListReplaced(ao: Tracks, o: CurrentTrack)

    @signal()
    def TrackListReplaced(self, tracks: 'ao', current_track: 'o') -> 'aoo':
        """Indicate that the entire tracklist has been replaced.

        It is left up to the implementation to decide when a change to the
        track list is invasive enough that this signal should be emitted
        instead of a series of 'TrackAdded' and 'TrackRemoved' signals.

        Parameters
        ----------
        tracks : [TrackId]
            The new content of the tracklist.
        current_track : TrackId
            The identifier of the track to be considered as current.

            "/org/mpris/MediaPlayer2/TrackList/NoTrack" indicates that there
            is no current track.

            This should correspond to the "mpris:trackid" field of the
            'Metadata' property of the "org.mpris.MediaPlayer2.Player"
            interface.

        Returns
        -------
        [[TrackId], TrackId]
            '[TrackId]':
                A list with the new content of the tracklist.
            'TrackId':
                The identifier of the track to be considered as current.

        """
        logger.info(
            'Signal org.mpris.MediaPlayer2.TrackList.TrackListReplaced'
            '(tracks=%s, current_track=%s) to emit',
            tracks, current_track)
        return [tracks, current_track]

    # TrackAdded(a{sv}: Metadata, o: AfterTrack)

    @signal()
    def TrackAdded(self, metadata: 'a{sv}', after_track: 'o') -> 'a{sv}o':
        """Indicate that a track has been added to the track list.

        Parameters
        ----------
        metadata : MetaData
            The metadata of the newly added item.

            This must include a "mpris:trackid" entry.
        after_track : TrackId
            The identifier of the track after which the new track was
            inserted. The path "/org/mpris/MediaPlayer2/TrackList/NoTrack"
            indicates that the track was inserted at the start of the track
            list.

        Returns
        -------
        [MetaData, TrackId]
            'MetaData':
                The metadata of the newly added item.
            'TrackId':
                The identifier of the track after which the new track was
                inserted.

        """
        logger.info(
            'Signal org.mpris.MediaPlayer2.TrackList.TrackAdded'
            '(metadata=%s, after_track=%s) to emit',
            metadata, after_track)
        return [metadata, after_track]

    # TrackRemoved(o: TrackId)

    @signal()
    def TrackRemoved(self, track_id: 'o') -> 'o':
        """Indicate that a track has been removed from the track list.

        Parameters
        ----------
        track_id : TrackId
            The identifier of the track being removed.

            "/org/mpris/MediaPlayer2/TrackList/NoTrack" is not a valid value
            for this argument.

        Returns
        -------
        TrackId
            The identifier of the track being removed.

        """
        logger.info(
            'Signal org.mpris.MediaPlayer2.TrackList.TrackRemoved'
            '(track_id=%s) to emit',
            track_id)
        return track_id

    # TrackMetadataChanged(o: TrackId, a{sv}: Metadata)

    @signal()
    def TrackMetadataChanged(self, track_id: 'o', metadata: 'a{sv}') -> 'oa{sv}':
        """Indicate that the metadata of a track in the tracklist has changed.

        This may indicate that a track has been replaced, in which case the
        "mpris:trackid" metadata entry is different from the 'track_id'
        argument.

        Parameters
        ----------
        track_id : TrackId
            The id of the track which metadata has changed.

            If the track id has changed, this will be the old value.

            "/org/mpris/MediaPlayer2/TrackList/NoTrack" is not a valid value
            for this argument.
        metadata : MetaData
            The new track metadata.

            This must include a "mpris:trackid" entry. If the track id has
            changed, this will be the new value.

        Returns
        -------
        [TrackId, MetaData]:
            'TrackId'
                The id of the track which metadata has changed.
            'MetaData'
                The new track metadata.

        """
        logger.info(
            'Signal org.mpris.MediaPlayer2.TrackList.TrackMetadataChanged'
            '(track_id=%s, metadata=%s) to emit',
            track_id, metadata)
        return [track_id, metadata]

    #
    # Properties
    #

    # Tracks                ao (Track_Id_List)      Read only

    @dbus_property(access=PropertyAccess.READ)
    async def Tracks(self) -> 'ao':
        """List with 'TrackId's of each track, in order.

        Signals
        -------
        org.freedesktop.DBus.Properties.PropertiesChanged
            This signal is emitted every time this property changes, but the
            signal message does not contain the new value. Client
            implementations should rather rely on the 'TrackAdded',
            'TrackRemoved' and 'TrackListReplaced' signals to keep their
            representation of the tracklist up to date.

        Returns
        -------
        [TrackId]
            A list with the track ids in the tracklist, in order.

        """
        logger.info(
            'Property org.mpris.MediaPlayer2.TrackList.Tracks requested')
        track_ids = await self._get_Tracks()
        return [self.mopidyid_to_dbusid(track_id) for track_id in track_ids]

    async def _get_Tracks(self):
        tl_tracks = await self.mopidy.tracklist.get_tl_tracks()
        return [tl_track['tlid'] for tl_track in tl_tracks]

    # CanEditTracks         b                       Read only

    @dbus_property(access=PropertyAccess.READ)
    def CanEditTracks(self) -> 'b':
        """Whether 'AddTrack()' and 'RemoveTrack()' can be called.

        Signals
        -------
        org.freedesktop.DBus.Properties.PropertiesChanged
            This signal is emitted with the new value every time this
            property changes.

        Returns
        -------
        bool
            False:
                Calling 'AddTrack()' or 'RemoveTrack()' will have no effect
                (and may raise a 'NotSupported' error).
            True:
                'AddTrack()' and 'RemoveTrack()' can be called.

        """
        logger.info(
            'Property '
            'org.mpris.MediaPlayer2.TrackList.CanEditTracks requested')
        return self._get_CanEditTracks()

    def _get_CanEditTracks(self):
        return True
