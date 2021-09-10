# This is a sample Python script.
import shutil
import gi

gi.require_version("Gtk", "3.0")

from gi.repository import Gtk, Gio, Gdk
from recorder import Recorder
from config import Config


class Handler:
    def onDestroy(self, *args):
        Gtk.main_quit()

    def on_btnMark_clicked(self, button):
        recorder.mark()

    def on_btnRec_clicked(self, button):
        if recorder.do_record:
            # is recording, so stop this one
            recorder.stop()
            win.get_style_context().remove_class("recording")
            builder.get_object("lblRecBtn").set_text("REC")
            builder.get_object("iconRecBtn").set_from_gicon(Gio.ThemedIcon(name="gtk-media-record"),
                                                            Gtk.IconSize.LARGE_TOOLBAR)
        else:
            # is not recording, so start a new one
            recorder.start()
            win.get_style_context().add_class("recording")
            builder.get_object("lblRecBtn").set_text("Stop")
            builder.get_object("iconRecBtn").set_from_gicon(Gio.ThemedIcon(name="gtk-media-stop"),
                                                            Gtk.IconSize.LARGE_TOOLBAR)

    def on_lblDiskSpace_draw(self, label, event):
        update_disk_space()

    def on_lblTimeRecording_draw(self, label, event):
        update_recording_time()


def update_recording_time():
    builder.get_object("lblTimeRecording").set_text(str(recorder.recordingTime).split('.', 2)[0])
    while Gtk.events_pending():
        Gtk.main_iteration()


def update_disk_space():
    label = builder.get_object("lblDiskSpace")
    icon = builder.get_object("iconDiskSpace")
    if label is not None:
        nDiskSpace = shutil.disk_usage(conf.recordingDirectory).free / 1000 ** 3
        if nDiskSpace > 1:
            # present as Gb
            strDiskSpace = str(round(nDiskSpace)) + " Gb"
            icon.set_from_gicon(Gio.ThemedIcon(name="dialog-ok"), Gtk.IconSize.BUTTON)
        else:
            # present as Mb, also set icon to warning as this generally means < 1 hr recording time left
            strDiskSpace = str(round(nDiskSpace * 1000)) + " Mb"
            icon.set_from_gicon(Gio.ThemedIcon(name="dialog-warning"), Gtk.IconSize.BUTTON)

        label.set_text("Disk space remaining: " + strDiskSpace)
        while Gtk.events_pending():
            Gtk.main_iteration()


if __name__ == '__main__':
    global conf
    global recorder

    conf = Config()
    recorder = Recorder(conf)

    builder = Gtk.Builder()
    builder.add_from_file("pycorder.glade")
    builder.connect_signals(Handler())

    provider = Gtk.CssProvider()
    css = b"""
    .recording {
        border-style: solid;
        border-width: 6px;
        border-color: red;
    }
    """
    provider.load_from_data(css)
    Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(),
                                             provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    win = builder.get_object("window1")
    win.show_all()

    Gtk.main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
