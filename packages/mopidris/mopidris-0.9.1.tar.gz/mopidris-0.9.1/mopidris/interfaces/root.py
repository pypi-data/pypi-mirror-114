"""The root MPRIS D-Bus interface for a remote Mopidy instance.

The D-Bus name of this interface is 'org.mpris.MediaPlayer2'.


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
import asyncio

import dbus_next as dbus
from dbus_next.service import method, dbus_property, PropertyAccess

from .base import _MopidyBaseInterface


logger = logging.getLogger(__name__)


class MopidyInterface(_MopidyBaseInterface):
    """The "org.mpris.MediaPlayer2" interface.

    See:
        https://specifications.freedesktop.org/mpris-spec/2.2/Media_Player.html
    """

    def __init__(self, mopidy, *args,
                 can_quit=False, loop_type='asyncio', **kwargs):
        """Inititalize the 'MopidyInterface' class.

        Parameters
        ----------
        mopdiy : mopidy_asyncio_client.MopidyClient
            The mopidy client
        can_quit : bool, optional
            If the program advertise, that it can be quit.
            The default is 'False'.
        loop_type : str, optional
            The type of the loop. Currently supported are "aiorun" and the
            standard "asyncio".
            The default is "asyncio".
        *args : arguments
            Passed on to parent class.
        **kwargs : keyword arguments
            Passed on to parent class.

        Returns
        -------
        None.

        """
        self._can_quit = can_quit
        logger.info(
            f'The program {"can not" if can_quit else "CAN"} quit')
        self._loop_type = loop_type
        logger.debug(
            f'The asyncio library used is: {loop_type}')
        super().__init__('org.mpris.MediaPlayer2',
                         mopidy, *args, **kwargs)

    #
    # Mopidy events
    #

    #
    # Methods
    #

    # Raise                                             → nothing

    @method()
    def Raise(self):
        """Bring the media player's user interface to the front.

        The media player may be unable to control how its user interface is
        displayed, or it may not have a graphical user interface at all. In
        this case, the 'CanRaise' property is 'False' and this method does
        nothing.

        Raises
        ------
        NotSupported
            May be raised, if the 'CanRaise' property is 'False'.

        Returns
        -------
        None.

        """
        logger.info(
            'Method org.mpris.MediaPlayer2.Raise() called')
        if self._get_CanRaise():
            pass
        else:
            dbus.DBusError(
                dbus.ErrorType.NOT_SUPPORTED,
                f'{self.mopidy} cannot raise a window, '
                f'because mopidy is running remotely')

    # Quit()                                            → nothing

    @method()
    async def Quit(self):
        """Cause the media player to stop running.

        The media player may refuse to allow clients to shut it down. In this
        case, the 'CanQuit' property is 'False' and this method does nothing.

        Raises
        ------
        NotSupported
            May be raised, if the 'CanQuit' property is 'False'.

        Returns
        -------
        None.

        """
        logger.info(
            'Method org.mpris.MediaPlayer2.Quit() called')
        if self._get_CanQuit():
            # Display quitting message
            # FIXME: Changed metadata is not displayed
            self.emit_properties_changed(
                Metadata={
                    'xesam:title': dbus.Variant('s', 'Quitting...'),
                    'xesam:artist': dbus.Variant('as', ['Quitting…'])})
            loop = asyncio.get_running_loop()
            if self._loop_type == 'aiorun':
                logging.debug(
                    "Shutting down using 'aiorun'")
                loop.stop()
            else:
                logging.debug(
                    "Shutting down using 'asyncio'")
                current_task = asyncio.current_task(loop)
                # Get running tasks
                tasks = [task
                         for task in asyncio.all_tasks(loop)
                         if task is not current_task]
                # Cancel all running tasks
                [task.cancel() for task in tasks]
                # Wait for the tasks to finish
                await asyncio.gather(*tasks)
                # Exit the loop
                loop.close()
            logging.info(
                'Shut down')
        else:
            dbus.DBusError(
                dbus.ErrorType.NOT_SUPPORTED,
                f'{self.mopidy} cannot quit, '
                f'because mopidy is running remotely')

    #
    # Properties
    #

    # CanQuit               b                       Read only

    @dbus_property(access=PropertyAccess.READ)
    def CanQuit(self) -> 'b':
        """Whether the media player can quit.

        Signals
        -------
        org.freedesktop.DBus.Properties.PropertiesChanged
            This signal is emitted with the new value every time this
            property changes.

        Returns
        -------
        bool
            'False':
                Calling 'Quit()' will have no effect, and may raise a
                'NotSupported' error.
            'True':
                Calling 'Quit()' will cause the media application to attempt
                to quit (although it may still be prevented from quitting by
                the user, for example).

        """
        logger.info(
            'Property org.mpris.MediaPlayer2.CanQuit requested')
        return self._get_CanQuit()

    def _get_CanQuit(self):
        return self._can_quit

    # Fullscreen            b                       Read/Write    (optional)

    @dbus_property(access=PropertyAccess.READWRITE)
    def Fullscreen(self) -> 'b':
        """Whether the media player is occupying the fullscreen.

        Signals
        -------
        org.freedesktop.DBus.Properties.PropertiesChanged
            This signal is emitted with the new value every time this
            property changes.

        Parameters
        ----------
        value : bool
            'False':
                Clients may set this property to 'False' to return to
                windowed mode.
            'True':
                Clients may set this property to 'True' to tell the media
                player to enter fullscreen mode.

            If 'CanSetFullscreen' is 'False', then attempting to set this
            property should have no effect, and may raise an error.
            However, even if it is 'True', the media player may still be
            unable to fulfil the request, in which case attempting to set
            this property will have no effect (but should not raise an
            error).

        Raises
        ------
        NotSupported
            May be raised, if the 'CanSetFullscreen' property is 'False'.

        Returns
        -------
        bool
            'False':
                The media player is not taking up the full screen.
            'True':
                The media player is taking up the full screen.

        """
        logger.info(
            'Property org.mpris.MediaPlayer2.Fullscreen requested')
        return self._get_Fullscreen()

    @Fullscreen.setter
    def Fullscreen(self, value: 'b'):
        logger.info(
            'Property org.mpris.MediaPlayer2.Fullscreen set to: %s',
            value)
        try:
            self._set_Fullscreen(value)
        except NotImplementedError:
            dbus.DBusError(
                dbus.ErrorType.NOT_SUPPORTED,
                f'{self.mopidy} cannot occupy fullscreen, '
                'because mopidy is running remotely')
            return False

    def _get_Fullscreen(self):
        return False

    def _set_Fullscreen(self, value):
        if self._get_CanSetFullscreen():
            self.emit_properties_changed(
                Fullscreen=bool(value))
        else:
            raise NotImplementedError

    # CanSetFullscreen      b                       Read only     (optional)

    @dbus_property(access=PropertyAccess.READ)
    def CanSetFullscreen(self) -> 'b':
        """Whether the media player can occupy the fullscreen.

        Signals
        -------
        org.freedesktop.DBus.Properties.PropertiesChanged
            This signal is emitted with the new value every time this
            property changes.

        Returns
        -------
        bool
            'False':
                Attempting to set 'Fullscreen' will have no effect, and may
                raise an error.
            'True':
                Attempting to set 'Fullscreen' will not raise an error, and
                (if it is different from the current value) will cause the
                media player to attempt to enter or exit fullscreen mode.

        """
        logger.info(
            'Property org.mpris.MediaPlayer2.CanSetFullscreen requested')
        return self._get_CanSetFullScreen()

    def _get_CanSetFullScreen(self):
        return False

    # CanRaise              b                       Read only

    @dbus_property(access=PropertyAccess.READ)
    def CanRaise(self) -> 'b':
        """Whether the media application can be raised.

        Signals
        -------
        org.freedesktop.DBus.Properties.PropertiesChanged
            This signal is emitted with the new value every time this
            property changes.

        Returns
        -------
        bool
            'False':
                Calling 'Raise()' will have no effect, and may raise a
                'NotSupported' error.
            'True':
                Calling 'Raise()' will cause the media application to attempt
                to bring its user interface to the front, although it may be
                prevented from doing so (by the window manager, for example).

        """
        logger.info(
            'Property org.mpris.MediaPlayer2.CanRaise requested')
        return self._get_CanRaise()

    def _get_CanRaise(self):
        return False

    # HasTrackList          b                       Read only

    @dbus_property(access=PropertyAccess.READ)
    def HasTrackList(self) -> 'b':
        """Whether the /org/mpris/MediaPlayer2 object implements
        the org.mpris.MediaPlayer2.TrackList interface.

        Signals
        -------
        org.freedesktop.DBus.Properties.PropertiesChanged
            This signal is emitted with the new value every time this
            property changes.

        Returns
        -------
        bool
            'False':
                The /org/mpris/MediaPlayer2 object does not implement the
                org.mpris.MediaPlayer2.TrackList interface.
            'True':
                The /org/mpris/MediaPlayer2 object implements the
                org.mpris.MediaPlayer2.TrackList interface.

        """
        logger.info(
            'Property org.mpris.MediaPlayer2.HasTrackList requested')
        return self._get_HasTrackList()

    def _get_HasTrackList(self):
        return True

    # Identity              s                       Read only

    @dbus_property(access=PropertyAccess.READ)
    def Identity(self) -> 's':                                  # noqa: D401
        """A friendly name to identify the media player to users.

        This should usually match the name found in .desktop files.

        Signals
        -------
        org.freedesktop.DBus.Properties.PropertiesChanged
            This signal is emitted with the new value every time this
            property changes.

        Returns
        -------
        str
            The user friendly name of the media player.

        """
        logger.info(
            'Property org.mpris.MediaPlayer2.Identity requested')
        return self._get_Identity()

    def _get_Identity(self):
        return str(self.mopidy)

    # DesktopEntry          s                       Read only     (optional)

    @dbus_property(access=PropertyAccess.READ)
    def DesktopEntry(self) -> 's':                              # noqa: D401
        """The basename of the installed .desktop file.

        Example
        -------
            The desktop entry file is '/usr/share/applications/vlc.desktop',
            and this property contains "vlc".

        Signals
        -------
        org.freedesktop.DBus.Properties.PropertiesChanged
            This signal is emitted with the new value every time this
            property changes.

        Returns
        -------
        str
            The basename of an installed .desktop file which complies with
            the Desktop entry specification, with the ".desktop" extension
            stripped.

        """
        logger.info(
            'Property org.mpris.MediaPlayer2.DesktopEntry requested')
        return self._get_DesktopEntry()

    def _get_DesktopEntry(self):
        return 'mopidris'

    # SupportedUriSchemes   as                      Read only

    @dbus_property(access=PropertyAccess.READ)
    async def SupportedUriSchemes(self) -> 'as':                # noqa: D401
        """The URI schemes supported by the media player.

        This can be viewed as protocols supported by the player in almost all
        cases. Almost every media player will include support for the "file"
        scheme. Other common schemes are "http" and "rtsp".

        Signals
        -------
        org.freedesktop.DBus.Properties.PropertiesChanged
            This signal is emitted with the new value every time this
            property changes.

        Returns
        -------
        [str]
            A list of the supported URI schemes (in lower-case).

        """
        logger.info(
            'Property org.mpris.MediaPlayer2.SupportedUriSchemes requested')
        return await self._get_SupportedUriSchemes()

    async def _get_SupportedUriSchemes(self):
        return await self.mopidy.core.get_uri_schemes()

    # SupportedMimeTypes   as                       Read only

    @dbus_property(access=PropertyAccess.READ)
    def SupportedMimeTypes(self) -> 'as':                       # noqa: D401
        """The mime-types supported by the media player.

        Signals
        -------
        org.freedesktop.DBus.Properties.PropertiesChanged
            This signal is emitted with the new value every time this
            property changes.

        Returns
        -------
        [str]
            A list of supported mime-types in the standard format (e.g.
            "audio/mpeg" or "application/ogg")

        """
        logger.info(
            'Property org.mpris.MediaPlayer2.SupportedMimeTypes requested')
        return self._get_SupportedMimeTypes()

    def _get_SupportedMimeTypes(self):
        # BUG: Supported MimeTypes are not exposed by mopidy
        # Issue:
        #   https://github.com/mopidy/mopidy/issues/812
        # PR has hard coded mime types:
        #   https://github.com/mopidy/mopidy-mpris/pull/11
        return [
            'audio/mpeg',
            'audio/x-ms-wma',
            'audio/x-ms-asf',
            'audio/x-flac',
            'audio/flac',
            'audio/l16;channels=2;rate=44100',
            'audio/l16;rate=44100;channels=2']
