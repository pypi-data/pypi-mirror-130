"""Base subparser module

Used by the `get`, `create`, and `cancel` subparsers.
"""

from __future__ import annotations

__all__ = ('Base', 'FormatEnum', 'ProgressEnum')

import abc
import enum
import logging
import re
import sys
from typing import TYPE_CHECKING

from . import ansi
from . import http
from .util import format_bytes, split_seconds

if TYPE_CHECKING:
    import argparse
    from collections.abc import Mapping
    from typing import Any, Optional, TextIO, TypeVar

    BaseT = TypeVar('BaseT', bound='Base')


class FormatEnum(enum.Enum):
    """Enum of possible values used by the `output_format` attribute"""
    PROGRESS = 'progress'
    ALL = 'all'
    JSON = 'json'


class ProgressEnum(enum.Enum):
    """Enum of possible values used by the `progress_mode` attribute"""
    OVERWRITE = 'overwrite'
    NEW_LINE = 'new_line'
    NONE = 'none'


class Base(abc.ABC):
    """Base subparser class that's used by the other subparser classes"""

    __slots__ = (
        'detach', 'interval', 'output_format', 'use_escape_codes',
        'output_file', 'progress_mode', 'opener'
    )

    detach: bool
    """If `True`, the class won't wait for the job to finish before
    exiting

    This has no effect if `output_format` isn't `progress`
    """
    interval: float
    """How frequently to poll the ytdl-server for status updates in
    seconds"""
    output_format: FormatEnum
    """Output format

    PROGRESS: Print recent logs and download progress. If `detach` is
        `False`, the newer logs and progress information will continue
        to be printed until the job finishes.
    ALL: Print all job information in a human-readable format.
    JSON: Print all job information as JSON.
    """
    use_escape_codes: bool
    """Whether or not to use ANSI escape codes

    Escape codes are used to colorized the output, and to delete the
    last line when displaying download progress.

    For download progress, the class will fall back to using whitespace
    to clear the line if this is `False`. You can disable overwriting
    progress via the `progress_mode` attribute.
    """
    progress_mode: ProgressEnum
    """Format to use when printing download progress

    OVERWRITE: Overwrite the last progress line so that only a single
        line is visible at a time. If `use_escape_codes` is `True`, the
        last line will be overwritten using escape codes; otherwise,
        the line will be overwritten by appending extra whitespace.
    NEW_LINE: Print each update as a new line.
    NONE: Do not print download progress.

    This has no effect if `output_format` isn't `progress`.
    """
    output_file: Optional[TextIO]
    """The IO stream to output youtube-dl logs and download progress to

    If set to `None`, nothing will be outputted.
    """

    opener: http.Opener
    """Opener instance used for communicating with the ytdl-server

    This should be generated via `http.Opener.from_env()`.
    """

    IN_PROGRESS_STATUSES = frozenset(('queued', 'downloading'))
    """Set of job statuses that indicate that the job is unfinished"""
    ERROR_STATUSES = frozenset(('error', 'timeout'))
    """Set of job statuses that indicate that the job failed"""

    LOG_COLORS = {
        'debug': ansi.FGColor.CYAN,
        'warning': ansi.FGColor.YELLOW,
        'error': ansi.FGColor.RED
    }
    """Map of log levels to their respective colors

    Log levels that aren't in this dict won't be colored.
    """

    LOG_REGEX_COLON = re.compile(
        r'(?P<header>\w+)(?P<after>:.+)'
    )
    """Regex used to match log lines in the format 'HEADER: MESSAGE'

    This is used to colorize the header of the message
    """
    LOG_REGEX_BRACKETS = re.compile(
        r'(?P<before>\[)(?P<header>\w+)(?P<after>\].+)'
    )
    """Regex used to match log lines in the format '[HEADER] MESSAGE'

    This is used to colorize the header of the message
    """

    def __init__(
        self, *, opener: http.Opener, detach: bool, interval: float,
        output_format: FormatEnum, use_escape_codes: bool,
        output_file: Optional[TextIO], progress_mode: ProgressEnum
    ) -> None:
        """Base initializer

        If you redefine this in a subclass, be sure to call this via
        `super().__init__()`.
        Also be sure to redefine `_get_kwargs()` if you add new kwargs.
        """
        self.opener = opener
        self.detach = detach
        self.interval = interval
        self.output_format = output_format
        self.use_escape_codes = use_escape_codes
        self.progress_mode = progress_mode
        self.output_file = output_file

    @classmethod
    def from_argparse(cls: type[BaseT], args: argparse.Namespace) -> BaseT:
        """Create an instance of the class based on the given argparse
        args

        The argparse namespace should be generated from
        `args.get_parser()`

        Raises `ArgumentError` if an argument has an invalid value
        """
        kwargs = cls._get_kwargs(args)
        logging.debug('Creating %s with kwargs: %s', cls.__name__, kwargs)
        return cls(**kwargs)

    @staticmethod
    def _get_kwargs(args: argparse.Namespace) -> dict[str, Any]:
        """Get the kwargs used by `from_argparse()` to create an
        instance

        If you want to add new kwargs in a subclass, redefine the method
        in your subclass as follows::

            @classmethod
            def _get_kwargs(cls, args: argparse.Namespace) -> dict[str, Any]:
                kwargs = super()._get_kwargs(args)
                # Add additional kwargs
                kwargs['new_arg'] = 'foo'
                return kwargs

        Note that it must be a @classmethod in order for `super()` to
        work
        """
        if args.quiet:
            output_file = None
        else:
            output_file = sys.stdout

        if args.color == 'always':
            use_escape_codes = True
        elif args.color == 'never':
            use_escape_codes = False
        else:  # args.color == 'auto'
            use_escape_codes = sys.stdout.isatty()

        if args.progress_format == 'auto':
            if sys.stdout.isatty():
                progress_mode = ProgressEnum.OVERWRITE
            else:
                progress_mode = ProgressEnum.NEW_LINE
        else:
            progress_mode = ProgressEnum(args.progress_format)

        opener = http.Opener.from_env(
            args.ytdl_server, args.ytdl_username, args.ytdl_password
        )

        kwargs = {
            'opener': opener,
            'detach': args.detach,
            'interval': args.interval,
            'output_format': FormatEnum(args.output_format),
            'use_escape_codes': use_escape_codes,
            'output_file': output_file,
            'progress_mode': progress_mode
        }
        return kwargs

    @abc.abstractmethod
    def start(self) -> None:
        """This method should be used to perform the primary action of
        the subparser, as well as print the output"""
        ...

    def format_log(self, log: Mapping[str, str]) -> str:
        """Format the given log entry into a user-readable str

        The header of the message is colorized if possible.
        """
        if log['level'] not in self.LOG_COLORS or not self.use_escape_codes:
            return log['message']

        for regex in (self.LOG_REGEX_COLON, self.LOG_REGEX_BRACKETS):
            match = regex.fullmatch(log['message'])
            if match:
                break
        else:
            # Message doesn't have a header that can be colorized
            return log['message']

        groups = match.groupdict(default='')
        color = self.LOG_COLORS[log['level']]

        header = ansi.format_fg_color(
            groups['header'], color, ansi.Brightness.BOLD
        )
        before = groups.get('before', '')
        after = groups.get('after', '')

        return f'{before}{header}{after}'

    @staticmethod
    def _format_download_progress(
        progress: Mapping[str, Any], pad: bool
    ) -> str:
        """Format the download progress when the status is 'downloading'

        If `pad` is `True`, extra whitespace will be added so that the
        length of the string is consistent.

        Example with pad:
            ' 58.9% of 210.7 KiB at    4.88 KiB/s ETA    00:17'
        Example without pad:
            '58.9% of 210.7 KiB at 4.88 KiB/s ETA 00:17'
        Example when the progress mapping has fragments:
            '58.9% of ~210.7 KiB at 4.88 KiB/s ETA 00:17 (frag 8/15)'

        Used by `format_progress()`.
        """
        prog_list: list[str] = []

        # If `True`, a tilde (~) will be prepended to the total bytes
        is_total_estimate = False

        total_bytes = progress.get('total_bytes', None)
        if total_bytes is None:
            total_bytes = progress.get('total_bytes_estimate', None)
            if total_bytes is not None:
                is_total_estimate = True

        downloaded_bytes = progress.get('downloaded_bytes', None)
        if downloaded_bytes is not None:
            if total_bytes is not None:
                percentage = round(downloaded_bytes / total_bytes * 100, 1)
                if pad:
                    prog_list.append(f'{percentage:>5}%')
                else:
                    prog_list.append(f'{percentage}%')
            else:
                prog_list.append(format_bytes(downloaded_bytes))
        else:
            prog_list.append('???.?%')

        prog_list.append('of')

        if total_bytes is not None:
            formatted_total = format_bytes(total_bytes)
            if is_total_estimate:
                with_tilde = f'~{formatted_total}'
                if pad:
                    prog_list.append(f'{with_tilde:>12}')
                else:
                    prog_list.append(with_tilde)
            else:
                # The total doesn't need to be padded when it's not an
                # estimate since it doesn't change.
                prog_list.append(formatted_total)
        else:
            prog_list.append('????.?? B')

        prog_list.append('at')

        speed = progress.get('speed', None)
        if speed is not None:
            formatted_speed = format_bytes(speed)
            if pad:
                prog_list.append(f'{formatted_speed:>11}/s')
            else:
                prog_list.append(f'{formatted_speed}/s')
        else:
            if pad:
                prog_list.append('  ????.?? B/s')
            else:
                prog_list.append('????.?? B/s')

        prog_list.append('ETA')

        eta = progress.get('eta', None)
        if eta is not None:
            hours, minutes, seconds = split_seconds(eta)
            if hours > 0:
                prog_list.append(
                    f'{hours:02d}:{minutes:02d}:{seconds:02d}'
                )
            elif pad:
                prog_list.append(f'   {minutes:02d}:{seconds:02d}')
            else:
                prog_list.append(f'{minutes:02d}:{seconds:02d}')
        else:
            prog_list.append('--:--')

        if 'fragment_index' in progress or 'fragment_count' in progress:
            fragment_index = progress.get('fragment_index', None)
            fragment_count = progress.get('fragment_count', None)

            if fragment_index is not None:
                fragment_index = str(fragment_index)
                fragment_pad_len = len(fragment_index)
            if fragment_count is not None:
                fragment_count = str(fragment_count)
                fragment_pad_len = len(fragment_count)

            if fragment_index is None:
                fragment_index = '?' * fragment_pad_len
            elif pad:
                fragment_index = fragment_index.rjust(fragment_pad_len)

            if fragment_count is None:
                fragment_count = '?' * fragment_pad_len
            elif pad:
                fragment_count = fragment_count.rjust(fragment_pad_len)

            prog_list.append(f'(frag {fragment_index}/{fragment_count})')

        return ' '.join(prog_list)

    @staticmethod
    def _format_finished_progress(progress: Mapping[str, Any]) -> str:
        """Format the finished download progress

        Example:
            171.23 KiB in 00:04

        Used by `format_progress()`.
        """
        prog_list: list[str] = []

        total_bytes = progress.get('total_bytes', None)
        if total_bytes is None:
            total_bytes = progress.get('total_bytes_estimate', None)

        # Add the total download size
        if total_bytes is not None:
            prog_list.append(f'{format_bytes(total_bytes)}')
        else:
            prog_list.append('????.?? B')

        prog_list.append('in')

        # Add the time elapsed
        elapsed = progress.get('elapsed', None)
        if elapsed is not None:
            hours, minutes, seconds = split_seconds(elapsed)
            if hours > 0:
                prog_list.append(
                    f'{hours:02d}:{minutes:02d}:{seconds:02d}'
                )
            else:
                prog_list.append(f'{minutes:02d}:{seconds:02d}')
        else:
            prog_list.append('--:--')

        return ' '.join(prog_list)

    @classmethod
    def format_progress(
        cls, progress: Mapping[str, Any], real_time: bool = True
    ) -> str:
        """Format the given progress entry into a user-readable str

        If `real_time` is `True`, the format will be formatted for
        real-time tracking by --output-format=progress. Otherwise, it
        will be formatted for --output-format=all.

        Examples when `real_time=True`:
            58.9% of 210.7 KiB at    4.88 KiB/s ETA    00:17

            Finished [171.23 KiB in 00:04] '1-1.ogg'

        Example when `real_time=False`:
            Downloading [58.9% of 210.7 KiB at 4.88 KiB/s ETA 00:17] '3-3.ogg'
        """
        if real_time and progress['status'] == 'downloading':
            return cls._format_download_progress(progress, pad=True)
        else:
            prog_list: list[str] = []

            prog_list.append(progress["status"].capitalize())
            prog_list.append(' [')

            if progress['status'] == 'downloading':
                download_progress = (
                    cls._format_download_progress(progress, pad=False)
                )
            else:
                download_progress = cls._format_finished_progress(progress)
            prog_list.append(download_progress)

            prog_list.append(f'] {progress["filename"]!r}')

            return ''.join(prog_list)

    def format_bold(self, text: Any) -> str:
        """Convert the given text to a bold string

        Returns the unformatted value if `user_color_codes` is `False`.
        """
        if self.use_escape_codes:
            return ansi.format_brightness(str(text))
        else:
            return str(text)

    def print(
        self, *values: Any, sep: str = ' ', end: str = '\n',
        flush: bool = False
    ) -> None:
        """Print the given values to `self.output_file`

        The function has no effect if `self.output_file` is `None`.

        Behavior is identical to the built-in `print()` function.
        """
        if self.output_file is None:
            return
        print(*values, file=self.output_file, sep=sep, end=end, flush=flush)
