"""Module containing the classes for storing and managing ALLPLAN plugins."""
from __future__ import annotations

import json
import warnings

from dataclasses import dataclass, field
from datetime import datetime
from enum import IntEnum, StrEnum
from pathlib import Path
from typing import cast
from uuid import UUID

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_Utility as AllplanUtil
import requests

from BuildingElement import BuildingElement
from FileNameService import FileNameService
from PythonPartActionBarUtil.YamlUtil.util import (_update_manifest_file, close_progress_bar, delete_folder, make_step_progress_bar, remove_directory,
                                                   sanitize_strings)

from . import config
from .allep import AllepPackage
from .installer import AllepInstaller
from .site_libraries.version import Version, InvalidVersion


class PluginsCollection:
    """Representation of a collection of ALLPLAN plugins."""

    branch = 'main' if AllplanSettings.AllplanVersion.MainReleaseName() == "9999" else AllplanSettings.AllplanVersion.MainReleaseName()

    def __init__(self, plugins: dict[UUID, Plugin] | None = None):
        """Initialization of the PluginsCollection.

        Args:
            plugins (dict[UUID, Plugin]): Dictionary with the
                plugins as values and their UUIDs as keys.
        """
        self._plugins = plugins if plugins is not None else dict()
        """Dictionary with the plugins as values and their UUIDs as keys."""

        self._sorted_uuids: list[UUID] = []
        """List of UUIDs in the alphabetical order of the plugins."""

    def append(self, plugin: Plugin):
        """Append a plugin to the collection.

        If the plugin is already in the collection, only its falsie attributes are updated.

        Args:
            plugin (Plugin): Plugin to append.
        """
        if plugin.uuid in self._plugins:
            for attr in plugin.__dataclass_fields__:
                if getattr(plugin, attr):
                    setattr(self._plugins[plugin.uuid], attr, getattr(plugin, attr))
        else:
            self._plugins[plugin.uuid] = plugin

        self._sort_plugins()

    def get_plugins_from_github(self):
        """ Get the plugins from the allplan-plugins.json file in the GitHub repository."""

        url = f'https://raw.githubusercontent.com/{config.PluginHubRepo.OWNER}/{config.PluginHubRepo.REPO}/{self.branch}/allplan-extensions.json'

        response = requests.get(url, timeout=10, headers=config.GITHUB_API_HEADERS)
        response.raise_for_status()
        plugin_list = response.json()

        for plugin_dict in plugin_list:
            self.append(Plugin(**plugin_dict))

        self._sort_plugins()

    def get_installed_plugins(self):
        """Get the plugins installed in Allplan.

        This method reads the manifests.json file from all the locations where plugins can be installed (usr, std, etc)
        and adds the plugins to the collection.
        """

        for location in InstallLocations:
            manifests_path = Path(FileNameService.get_global_standard_path(f"{location}\\AllepPlugins\\manifests.json"))

            if not manifests_path.exists():
                continue

            with open(manifests_path, encoding = "UTF-8") as file:
                manifest_data = json.load(file)

                for plugin in manifest_data["plugins"]:
                    self.append(Plugin(
                        uuid              = plugin["UUID"],
                        name              = plugin["pluginName"],
                        developer         = plugin["developerName"],
                        installed_date    = datetime.fromisoformat(plugin["createdOn"]),
                        installed_version = Version(plugin["version"]),
                        installed_files   = plugin["filesCopied"] + [plugin["ACTBFile"], plugin["NPDFile"]],
                        location          = location,
                    ))

    def update_building_element(self, build_ele: BuildingElement, only_status: bool = False):
        """Populate the building element with the plugin information.

        Args:
            build_ele (BuildingElement): Building element to populate.
            only_status (bool): If True, only the status of the plugins is updated, otherwise all the plugin information is updated.
        """
        build_ele.PluginStates.value        = [plgn.status for plgn in self]

        if only_status:
            return

        build_ele.PluginNames.value         = [plgn.name for plgn in self]
        build_ele.PluginDescriptions.value  = [plgn.description for plgn in self]
        build_ele.PluginHasGitHubRepo.value = [plgn.has_github for plgn in self]

    def clean_up(self):
        """Remove the plugins from the collection, that are not installed and don't have a GitHub repository."""
        self._plugins = {uuid: plugin for uuid, plugin in self._plugins.items() if plugin.status != PluginStatus.NOT_INSTALLED or plugin.has_github}
        self._sort_plugins()

    def _sort_plugins(self):
        """Sort the plugins by their names."""
        self._sorted_uuids = sorted(self._plugins, key=lambda uuid: self._plugins[uuid].name)

    def __getitem__(self, key: UUID | int) -> Plugin:   # pylint: disable=W9015,W9011
        """Get a plugin by its UUID."""
        if isinstance(key, int):
            return self._plugins[self._sorted_uuids[key]]
        return self._plugins[key]

    def __iter__(self):         # pylint: disable=W9011,W9012
        """Iterate over the plugins in alphabetical order of the plugin names."""
        return iter(self._plugins[uuid] for uuid in self._sorted_uuids)

    def __len__(self) -> int:   # pylint: disable=W9015,W9011
        """Get the number of plugins."""
        return len(self._plugins)

    def __repr__(self):         # pylint: disable=W9011,W9012
        """Representation of the PluginsCollection."""
        return f"{self.__class__.__name__}({self._plugins})"


class PluginStatus(IntEnum):
    """Enum to represent the status of an plugin. Used to show correct UI elements in the PythonPart palette."""

    NOT_INSTALLED = 0
    """Plugin is not installed."""

    INSTALLED = 1
    """Plugin is installed, but unknown whether the latest version."""

    UPDATE_AVAILABLE = 2
    """Plugin is installed, but an update is available."""

    UP_TO_DATE = 3
    """Plugin is installed and up to date."""


class InstallLocations(StrEnum):
    """Enum to represent the possible locations, where plugins can be installed."""

    ETC = "etc"
    """Plugins installed in the etc folder."""

    STD = "std"
    """Plugins installed in the std folder."""

    USR = "usr"
    """Plugins installed in the usr folder."""


@dataclass
class Plugin:
    """Dataclass to represent an ALLPLAN plugin.

    Attributes:
        uuid (UUID): UUID of the plugin.
        name (str): Name of the plugin.
        description (str): Short description of the plugin.
        github (dict): Dictionary with the GitHub repository information.
    """
    # Required attributes
    uuid              : UUID
    name              : str
    developer         : str

    # Optional attributes
    description       : str                     = ""
    github            : dict | None             = field(default=None)
    installed_date    : datetime | None         = field(default=None)
    installed_files   : set[Path]               = field(default_factory=set)
    installed_version : Version | None          = field(default=None)
    location          : InstallLocations | None = field(default=None)
    local_file        : Path | None             = field(default=None)

    # Internal attributes
    _latest_version     : Version | None      = field(init=False, default=None)
    _last_version_check : datetime | None     = field(init=False, default=None, repr=False, compare=False)
    _allep_package      : AllepPackage | None = field(init=False, default=None)

    def __post_init__(self):
        """Post initialization of the Plugin object."""
        # when getting plugins from github, uuid is a string
        if isinstance(self.uuid, str):
            self.uuid = UUID(self.uuid)

        # when getting installed files from the manifest file, they are strings and have some issues
        if len(self.installed_files) > 0 and any(isinstance(item, str) for item in self.installed_files):
            self.installed_files = set(self.installed_files)
            installed_files = cast(set[str], set(self.installed_files))
            self.installed_files.clear()

            for path in installed_files:
                if path.startswith("Usr"):
                    parts = path.split("\\")
                    parts.pop(1)
                    path = "\\".join(parts)

                absolute_path = Path(FileNameService.get_global_standard_path(path))

                if absolute_path.exists() and absolute_path.is_file():
                    self.installed_files.add(absolute_path)


    def check_latest_release(self):
        """Check the latest version of the plugin.

        Raises:
            requests.HTTPError: If the request to the GitHub API fails.
            ValueError: If the plugin does not have a GitHub repository or if no ALLEP package is found in the release assets
        """
        if not self.has_github:
            raise ValueError("Plugin does not have a GitHub repository attached.")

        url = f"https://api.github.com/repos/{self.github["owner"]}/{self.github["repo"]}/releases/latest"

        response = requests.get(url, timeout=10, headers=config.GITHUB_API_HEADERS)
        response.raise_for_status()
        release = response.json()

        self._last_version_check = datetime.now()
        try:
            self._latest_version = Version(release["tag_name"])
        except InvalidVersion as err:
            raise InvalidVersion(f"The latest release has a version in an invalid format ({release["tag_name"]}). Please inform the developer.") from err

        for asset in release["assets"]:
            if asset["name"].lower().endswith(".allep"):
                self._allep_package = AllepPackage(
                    name = asset["name"],
                    url = asset["browser_download_url"],
                    size = asset["size"])
                break
            raise ValueError("No ALLEP package found in the latest release of this plugin on GitHub.")

    def install(self, progress_bar: AllplanUtil.ProgressBar | None = None):
        """Install the plugin.

        Args:
            progress_bar: Instance of progress_bar. Defaults to None.
        """

        if self.allep_package is None:
            self.check_latest_release()

        installer = AllepInstaller(self.allep_package)
        installer.download_and_install_package(progress_bar)

        self.installed_version = self.latest_version
        self.installed_date    = datetime.now()

    def uninstall(self, progress_bar: AllplanUtil.ProgressBar | None = None):
        """ Uninstall the plugin.

        Args:
            progress_bar: Instance of progress_bar. Defaults to None.

        Warns:
            ResourceWarning: If a certain file is being used by another process and cannot be removed.
        """

        if self.status == PluginStatus.NOT_INSTALLED:
            return

        folder_path   = Path(FileNameService.get_global_standard_path(f"{self.location}\\"))   # type: ignore

        # Remove files
        make_step_progress_bar(40, "Removing files", progress_bar)

        while self.installed_files:
            if not (file := self.installed_files.pop()):
                continue

            try:
                file.unlink()
            except PermissionError as e:
                warnings.warn(f"File {file} is being used by another process and won't be removed. {e}", ResourceWarning)

        for folder in ("Library", "PythonPartsScripts", "PythonPartsActionbar"):
            plugin_directory = folder_path / folder / "AllepPlugins" / sanitize_strings(self.developer) / sanitize_strings(self.name)
            make_step_progress_bar(10, "Removing directories", progress_bar)
            remove_directory(str(plugin_directory))
            delete_folder(str(plugin_directory.parent))

        make_step_progress_bar(10, "Updating manifest files", progress_bar)
        _update_manifest_file(self.location.capitalize(), {"UUID": str(self.uuid)})
        self.installed_date = None
        self.installed_version = None

        make_step_progress_bar(10, "Completed", progress_bar)
        close_progress_bar(progress_bar)

    @property
    def allep_package(self) -> AllepPackage | None:
        """Get the ALLEP package attached to the latest release.

        Returns:
            AllepPackage: ALLEP package attached to the latest release.
        """
        return self._allep_package

    @property
    def has_github(self) -> bool:
        """Check if the plugin has a GitHub repository attached.

        Returns:
            bool: True if the plugin has a GitHub repository attached, False otherwise.
        """
        return self.github is not None

    @property
    def is_on_actionbar(self) -> bool:
        """Check if the plugin is integrated on the Actionbar.

        Returns:
            bool: True if the plugin is integrated to the Actionbar, False otherwise.
        """
        if self.status == PluginStatus.NOT_INSTALLED:
            return False

        return any(file.name.lower().endswith(".actb") for file in self.installed_files)

    @property
    def latest_version(self) -> Version:
        """Get the latest version of the plugin.

        Returns:
            Version: Latest version of the plugin.

        Raises:
            RuntimeError: If the plugin does not have a GitHub repository attached
        """
        if not self.has_github:
            raise RuntimeError("Cannot get the latest version of the plugin because there is no GitHub repository attached.")
        return cast(Version, self._latest_version)

    @property
    def status(self) -> PluginStatus:
        """Get the status of the plugin.

        Returns:
            PluginStatus: Status of the plugin.
        """
        if self.installed_version is None:
            return PluginStatus.NOT_INSTALLED

        if self._latest_version is not None:
            if self.installed_version < self._latest_version:
                return PluginStatus.UPDATE_AVAILABLE
            return PluginStatus.UP_TO_DATE
        return PluginStatus.INSTALLED
