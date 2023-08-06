"""Normcap main window."""
import os
import tempfile
import textwrap
import time
from typing import Dict, Tuple

from PySide2 import QtCore, QtGui, QtWidgets

from normcap import __version__, clipboard
from normcap.enhance import enhance_image
from normcap.gui.settings_menu import SettingsButton
from normcap.gui.system_tray import create_system_tray
from normcap.logger import logger
from normcap.magic import apply_magic
from normcap.models import (
    FILE_ISSUE_TEXT,
    Capture,
    CaptureMode,
    Config,
    DesktopEnvironment,
    DisplayManager,
    Platform,
    Rect,
    SystemInfo,
)
from normcap.ocr import perform_ocr
from normcap.screengrab import grab_screen
from normcap.update import get_new_version
from normcap.utils import get_icon, set_cursor
from normcap.window_base import WindowBase


class Communicate(QtCore.QObject):
    """Applications' communication bus."""

    onRegionSelected = QtCore.Signal(Rect)
    onImageGrabbed = QtCore.Signal()
    onOcrPerformed = QtCore.Signal()
    onImagePrepared = QtCore.Signal()
    onCopiedToClipboard = QtCore.Signal()
    onWindowPositioned = QtCore.Signal()
    onMinimizeWindows = QtCore.Signal()
    onSetCursorWait = QtCore.Signal()
    onQuitOrHide = QtCore.Signal()
    onMagicsApplied = QtCore.Signal()
    onUpdateAvailable = QtCore.Signal(str)


class WindowMain(WindowBase):
    """Main (parent) window."""

    tray: QtWidgets.QSystemTrayIcon

    def __init__(
        self,
        config: Config,
        system_info: SystemInfo,
    ):
        super().__init__(
            system_info=system_info, screen_idx=0, parent=None, color=config.color
        )
        self.config: Config = config
        self.capture: Capture = Capture()
        self.com = Communicate()

        self.all_windows: Dict[int, WindowBase] = {0: self}
        self.multi_monitor_mode = len(self.system_info.screens) > 1

        self._set_signals()

        self.settings_button = SettingsButton(self)
        self.settings_button.show()

        self.main_window.tray = create_system_tray(self)
        if self.config.tray:
            logger.debug("Show tray icon")
            self.main_window.tray.show()

        if self.config.updates:
            QtCore.QTimer.singleShot(0, self.check_for_updates)

        if self.multi_monitor_mode:
            self._init_child_windows()

    def _set_signals(self):
        """Setup signals to trigger program logic."""
        self.com.onRegionSelected.connect(self.grab_image)
        self.com.onImageGrabbed.connect(self.prepare_image)
        self.com.onImagePrepared.connect(self.capture_to_ocr)
        self.com.onOcrPerformed.connect(self.apply_magics)
        self.com.onMagicsApplied.connect(self.copy_to_clipboard)
        self.com.onCopiedToClipboard.connect(self.send_notification)

        self.com.onMinimizeWindows.connect(self.minimize_windows)
        self.com.onSetCursorWait.connect(lambda: set_cursor(QtCore.Qt.WaitCursor))
        self.com.onQuitOrHide.connect(self.quit_or_minimize)
        self.com.onUpdateAvailable.connect(self.show_update_message)

    ###################
    # UI Manipulation #
    ###################

    def _init_child_windows(self):
        """Initialize child windows with method depending on system."""
        if self.system_info.display_manager != DisplayManager.WAYLAND:
            self.create_all_child_windows()
        elif self.system_info.desktop_environment == DesktopEnvironment.GNOME:
            self.com.onWindowPositioned.connect(self.create_next_child_window)
        else:
            logger.error(
                f"NormCap currently doesn't support multi monitor mode"
                f"for {self.system_info.display_manager} "
                f"on {self.system_info.desktop_environment}."
                f"\n{FILE_ISSUE_TEXT}"
            )

    def create_next_child_window(self):
        """Instantiate child windows in multi screen setting."""
        if len(self.system_info.screens) > len(self.all_windows):
            index = max(self.all_windows.keys()) + 1
            self.create_child_window(index)

    def create_all_child_windows(self):
        """Opening all child windows at once."""
        for index in self.system_info.screens:
            if index == self.screen_idx:
                continue
            self.create_child_window(index)

    def create_child_window(self, index: int):
        """Open a child window for the specified screen."""
        self.all_windows[index] = WindowBase(
            system_info=self.system_info,
            screen_idx=index,
            parent=self,
            color=self.config.color,
        )
        self.all_windows[index].show()

    def minimize_windows(self):
        """Hide all windows of normcap."""
        set_cursor(None)
        for window in self.all_windows.values():
            window.hide()

    def show_windows(self):
        """Make hidden windows visible again."""
        for window in self.all_windows.values():
            if self.system_info.platform == Platform.MACOS:
                window.show()
                window.raise_()
                window.activateWindow()
            else:
                window.showFullScreen()

    def quit_or_minimize(self):
        """Minimize application if in tray-mode, else exit."""
        # Necessary to get text to clipboard before exitting
        if self.config.tray:
            logger.debug("Hiding windows to tray")
            self.minimize_windows()
        else:
            logger.debug("Hiding tray & processing events")
            self.main_window.tray.hide()
            QtWidgets.QApplication.processEvents()
            time.sleep(0.05)
            logger.debug(
                "Images have been saved for debugging in: "
                + f"{tempfile.gettempdir()}{os.sep}normcap"
            )
            logger.debug("Exit normcap.")
            QtWidgets.QApplication.quit()

    def show_or_hide_tray_icon(self):
        """Set visibility state of tray icon"""
        if self.config.tray:
            logger.debug("Show tray icon")
            self.main_window.tray.show()
        else:
            logger.debug("Hide tray icon")
            self.main_window.tray.hide()

    #########################
    # On settings change    #
    #########################

    def set_config(self, name, value):
        """Change value in config object."""
        logger.debug(f"Setting config {name} {value}")
        if name == "languages":
            languages = list(self.config.languages)
            action = [a for a in self.settings_menu.actions() if a.text() == value][0]
            checked = action.isChecked()
            if checked and value not in languages:
                languages.append(value)
            if not checked and value in languages:
                if len(languages) > 1:
                    languages.remove(value)
                else:
                    action.setChecked(True)
            self.config.languages = tuple(languages)
        elif name == "tray":
            self.config.__setattr__(name, value)
            self.show_or_hide_tray_icon()
        else:
            self.config.__setattr__(name, value)

        logger.debug(self.config)

    #########################
    # Checking for Updates  #
    #########################

    def check_for_updates(self):
        """Check if update is available and present dialog."""
        logger.debug("Checking for updates")

        new_version = get_new_version(self.system_info.briefcase_package)

        if not new_version:
            return

        self.com.onUpdateAvailable.emit(new_version)

    def show_update_message(self, new_version):
        """Show dialog informing about available update."""

        text = f"<b>NormCap v{new_version} is available.</b> (You have v{__version__})"
        if self.system_info.briefcase_package:
            info_text = (
                "You can download the new version for your operating system from "
                "GitHub.\n\n"
                "Do you want to visit the release website now?"
            )
        else:
            info_text = (
                "You should be able to upgrade from command line with "
                "'pip install normcap --upgrade'.\n\n"
                "Do you want to visit the release website now?"
            )

        msgBox = QtWidgets.QMessageBox()
        msgBox.setIconPixmap(get_icon("normcap.png").pixmap(48, 48))
        msgBox.setText(text)
        msgBox.setInformativeText(info_text)
        msgBox.setStandardButtons(
            QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel
        )
        msgBox.setDefaultButton(QtWidgets.QMessageBox.Ok)

        choice = msgBox.exec_()
        if choice == 1024:
            QtGui.QDesktopServices.openUrl("https://github.com/dynobo/normcap/releases")
            self.com.onQuitOrHide.emit()

    #########################
    # On notification send  #
    #########################

    def send_notification(self):
        """Setting up tray icon."""
        if not self.config.notifications:
            self.com.onQuitOrHide.emit()

        on_windows = self.system_info.platform == Platform.WINDOWS
        icon_file = "normcap.png" if on_windows else "tray.png"
        notification_icon = get_icon(icon_file, "tool-magic-symbolic")

        title, message = self.compose_notification()
        self.main_window.tray.show()
        self.main_window.tray.showMessage(title, message, notification_icon)

        # Delay quit or hide to get notification enough time to show up.
        delay = 5000 if self.system_info.platform == Platform.WINDOWS else 500
        QtCore.QTimer.singleShot(delay, self.com.onQuitOrHide.emit)

    def compose_notification(self) -> Tuple[str, str]:
        """Extract message text out of captures object and include icon."""
        # Message text
        text = self.capture.transformed.replace(os.linesep, " ")
        text = textwrap.shorten(text, width=45)
        if len(text) < 1:
            text = "Please try again."

        # Message title
        title = ""
        count = 0
        if len(self.capture.transformed) < 1:
            title += "Nothing!"
        elif self.capture.best_magic == "ParagraphMagic":
            count = self.capture.transformed.count(os.linesep * 2) + 1
            title += f"{count} paragraph"
        elif self.capture.best_magic == "EmailMagic":
            count = self.capture.transformed.count("@")
            title += f"{count} email"
        elif self.capture.best_magic == "SingleLineMagic":
            count = self.capture.transformed.count(" ") + 1
            title += f"{count} word"
        elif self.capture.best_magic == "MultiLineMagic":
            count = self.capture.transformed.count("\n") + 1
            title += f"{count} line"
        elif self.capture.best_magic == "UrlMagic":
            count = self.capture.transformed.count("http")
            title += f"{count} URL"
        elif self.capture.mode == CaptureMode.RAW:
            count = len(self.capture.transformed)
            title += f"{count} char"
        title += f"{'s' if count > 1 else ''} captured"

        return title, text

    #####################
    # OCR Functionality #
    #####################

    def grab_image(self, grab_info: Tuple[Rect, int]):
        """Get image from selected region."""
        logger.debug(f"Taking screenshot on {grab_info[0].points}")
        self.capture.rect = grab_info[0]
        self.capture.screen = self.system_info.screens[grab_info[1]]
        self.capture = grab_screen(
            system_info=self.system_info,
            capture=self.capture,
        )
        self.com.onImageGrabbed.emit()

    def prepare_image(self):
        """Enhance image before performin OCR."""
        if self.capture.image_area > 25:
            logger.debug("Preparing image for OCR")
            self.capture = enhance_image(self.capture)
            self.com.onImagePrepared.emit()
        else:
            logger.warning(f"Area of {self.capture.image_area} too small. Skip OCR.")
            self.com.onQuitOrHide.emit()

    def capture_to_ocr(self):
        """Perform content recognition on grabed image."""
        logger.debug("Performing OCR")
        self.capture = perform_ocr(
            languages=self.config.languages,
            capture=self.capture,
            system_info=self.system_info,
        )
        logger.info(f"Raw text from OCR:\n{self.capture.text}")
        logger.debug(f"Result from OCR:{self.capture}")
        self.com.onOcrPerformed.emit()

    def apply_magics(self):
        """Beautify/parse content base on magic rules."""
        if self.capture.mode is CaptureMode.PARSE:
            logger.debug("Applying Magics")
            self.capture = apply_magic(self.capture)
            logger.debug(f"Result from applying Magics:{self.capture}")
        if self.capture.mode is CaptureMode.RAW:
            logger.debug("Raw mode. Skip applying Magics and use raw text.")
            self.capture.transformed = self.capture.text.strip()
        self.com.onMagicsApplied.emit()

    def copy_to_clipboard(self):
        """Copy results to clipboard."""
        logger.info(f"Copying text to clipboard:\n{self.capture.transformed}")
        clipboard_copy = clipboard.init()
        clipboard_copy(self.capture.transformed)

        QtWidgets.QApplication.processEvents()
        time.sleep(1.05)
        self.com.onCopiedToClipboard.emit()
