import locale
import logging
import sys
import importlib
from optparse import Values
from typing import List, Set, Dict, OrderedDict, Optional, Any
from html.parser import HTMLParser

import os
from pip._internal.configuration import Configuration
from pip._vendor.packaging.version import parse as parse_version
from pip._internal.network.session import PipSession
from pip._internal.exceptions import NetworkConnectionError
from pip._internal.commands import CommandInfo
from pip._internal.cli.main_parser import parse_command
from pip._internal.exceptions import PipError

from pip._internal.cli.base_command import Command
from pip._internal.cli.req_command import SessionCommandMixin
from pip._internal.cli.status_codes import NO_MATCHES_FOUND, SUCCESS
from pip._internal.exceptions import CommandError
from pip._internal.models.link import Link
from pip._internal.network.download import _http_get_download
from pip._internal.utils.misc import write_output
from pip._internal.commands import commands_dict

logger = logging.getLogger(__name__)


commands_dict["versions"] = CommandInfo(
    "pip_plugin_versions.versions",
    "VersionsCommand",
    "Show available versions.",
)


class HTTPGetter:
    def __init__(
        self,
        session: PipSession,
        progress_bar: str,
    ) -> None:
        self._session = session
        self._progress_bar = progress_bar

    def __call__(self, link: Link) -> str:
        """Download the file given by link into location."""
        try:
            resp = _http_get_download(self._session, link)
        except NetworkConnectionError as e:
            assert e.response is not None
            logger.critical(
                "HTTP error %s while getting %s", e.response.status_code, link
            )
            raise

        return resp.text


class VersionsPageParser(HTMLParser):
    def __init__(self, package_name: str):
        super().__init__()
        self._versions = set()
        self._handle_link_content = False
        self._package_name = package_name

    @property
    def versions(self):
        return self._versions

    def handle_starttag(self, tag, _):
        if tag == "a":
            self._handle_link_content = True

    def handle_endtag(self, tag):
        if tag == "a":
            self._handle_link_content = False

    def handle_data(self, data):
        if self._handle_link_content:
            if data.endswith(".whl"):
                data = data.split("-py3")[0]
                data = data.split("-py2")[0]
                data = data.replace(self._package_name + "-", "")
                self._versions.add(data)
            elif data.endswith(".tar.gz"):
                data = data.replace(self._package_name + "-", "")
                data = data.replace(".tar.gz", "")
                self._versions.add(data)


class VersionsCommand(Command, SessionCommandMixin):
    """List of versions available for package whose name is <query>."""

    usage = """
      %prog [options] <query>"""
    ignore_require_venv = True

    def add_options(self) -> None:
        self.cmd_opts.add_option(
            '-i', '--index',
            dest='index',
            metavar='URL',
            default="",
            help='Base URL of Python Package Index (default %default)')

        self.parser.insert_option_group(0, self.cmd_opts)

    def run(self, options: Values, args: List[str]) -> int:
        if not args:
            raise CommandError("Missing required argument (search query).")
        hits = self.search(args[0], options)
        print_results(hits)
        if hits:
            return SUCCESS
        return NO_MATCHES_FOUND

    def search(self, query: str, options: Values) -> Set[str]:
        if options.index:
            index_url = options.index
        else:
            configuration = Configuration(isolated=False)
            configuration.load()
            index_url = configuration.get_value("global.index-url")

        if not index_url.endswith("/"):
            index_url = index_url + "/"

        session = self.get_default_session(options)

        getter = HTTPGetter(session, "off")
        data = getter(link=Link(index_url + query + "/"))
        vpp = VersionsPageParser(query)
        vpp.feed(data=data)

        return vpp.versions


def print_results(hits: List[str]) -> None:
    hits = sorted(hits, key=parse_version)
    if not hits:
        return
    for hit in hits:
        try:
            write_output(hit)
        except UnicodeEncodeError:
            pass


def create_command(name: str, **kwargs: Any) -> Command:
    """
    Create an instance of the Command class with the given name.
    """
    module_path, class_name, summary = commands_dict[name]
    module = importlib.import_module(module_path)
    command_class = getattr(module, class_name)
    command = command_class(name=name, summary=summary, **kwargs)

    return command


def main_plugin(args: Optional[List[str]] = None) -> int:
    if args is None:
        args = sys.argv[1:]

    try:
        cmd_name, cmd_args = parse_command(args)
    except PipError as exc:
        sys.stderr.write(f"ERROR: {exc}")
        sys.stderr.write(os.linesep)
        sys.exit(1)

    # Needed for locale.getpreferredencoding(False) to work
    # in pip._internal.utils.encoding.auto_decode
    try:
        locale.setlocale(locale.LC_ALL, "")
    except locale.Error as e:
        # setlocale can apparently crash if locale are uninitialized
        logger.debug("Ignoring error %s when setting locale", e)
    command = create_command(cmd_name, isolated=("--isolated" in cmd_args))

    return command.main(cmd_args)


def main():
    sys.argv[0] = "versions"
    args = sys.argv

    try:
        cmd_name, cmd_args = parse_command(args)
    except PipError as exc:
        sys.stderr.write(f"ERROR: {exc}")
        sys.stderr.write(os.linesep)
        sys.exit(1)

    # Needed for locale.getpreferredencoding(False) to work
    # in pip._internal.utils.encoding.auto_decode
    try:
        locale.setlocale(locale.LC_ALL, "")
    except locale.Error as e:
        # setlocale can apparently crash if locale are uninitialized
        logger.debug("Ignoring error %s when setting locale", e)
    command = create_command(cmd_name, isolated=("--isolated" in cmd_args))

    return command.main(cmd_args)


if __name__ == "__main__":
    main()
