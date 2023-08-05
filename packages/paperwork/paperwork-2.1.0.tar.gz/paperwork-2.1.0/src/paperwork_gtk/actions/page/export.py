import logging

try:
    from gi.repository import Gio
    GLIB_AVAILABLE = True
except (ImportError, ValueError):
    GLIB_AVAILABLE = False

import openpaperwork_core
import openpaperwork_core.deps


LOGGER = logging.getLogger(__name__)
ACTION_NAME = "page_export"


class Plugin(openpaperwork_core.PluginBase):
    def __init__(self):
        super().__init__()
        self.active_doc = None
        self.active_page_idx = -1
        self.active_windows = []

    def get_interfaces(self):
        return [
            'action',
            'action_page',
            'action_page_export',
            'chkdeps',
            'doc_open',
        ]

    def get_deps(self):
        return [
            {
                'interface': 'app_actions',
                'defaults': ['paperwork_gtk.mainwindow.window'],
            },
            {
                'interface': 'gtk_exporter',
                'defaults': ['paperwork_gtk.mainwindow.exporter'],
            },
        ]

    def init(self, core):
        super().init(core)
        if not GLIB_AVAILABLE:
            return

        action = Gio.SimpleAction.new(ACTION_NAME, None)
        action.connect("activate", self._open_exporter)
        self.core.call_all("app_actions_add", action)

    def chkdeps(self, out: dict):
        if not GLIB_AVAILABLE:
            out['glib'].update(openpaperwork_core.deps.GLIB)

    def doc_open(self, doc_id, doc_url):
        self.active_doc = (doc_id, doc_url)

    def doc_close(self):
        self.active_doc = None

    def on_page_shown(self, page_idx):
        self.active_page_idx = page_idx

    def _open_exporter(self, *args, **kwargs):
        assert(self.active_doc is not None)
        self.core.call_all(
            "gtk_open_exporter", *self.active_doc, self.active_page_idx
        )
