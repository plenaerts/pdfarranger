from gi.repository import Gtk
import gettext

_ = gettext.gettext


class Page_Dialog(Gtk.Dialog):
    """A dialog box to choose the page to sign."""

    def __init__(self, selection, window):
        super().__init__(
            title=_("Choose page to sign"),
            parent=window,
            flags=Gtk.DialogFlags.MODAL,
            buttons=(Gtk.STOCK_GOTO_FIRST, 1,
                     Gtk.STOCK_GOTO_LAST, 2,
                     Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL
                     ),
        )
        self.selection = selection
        self.label = Gtk.Label(
            _("Multiple pages selected. Choose one to sign."))
        self.vbox.pack_start(self.label, True, True, 6)
        self.show_all()
        self.set_default_response(Gtk.ResponseType.CANCEL)

    def run_get(self):
        """If user selected multiple pages, let him choose between the first,
        the last, or to choose again."""
        result = self.run()
        r = None
        if result == 1:
            r = min(self.selection)
        elif result == 2:
            r = max(self.selection)
        elif result == Gtk.ResponseType.CANCEL:
            r = None
        self.destroy()
        return r
