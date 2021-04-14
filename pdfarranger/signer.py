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


class _Position_Widget(Gtk.HBox):
    """A form to specify the position of the signature on a page."""

    def __init__(self):
        super().__init__()
        label_x1 = Gtk.Label(label="x1:")
        label_x2 = Gtk.Label(label="x2:")
        label_y1 = Gtk.Label(label="y1:")
        label_y2 = Gtk.Label(label="y2:")
        self.entry_x1 = Gtk.Entry(text="75", width_chars=3)
        self.entry_x2 = Gtk.Entry(text="175", width_chars=3)
        self.entry_y1 = Gtk.Entry(text="250", width_chars=3)
        self.entry_y2 = Gtk.Entry(text="285", width_chars=3)
        self.pack_start(label_x1, True, True, 6)
        self.pack_start(self.entry_x1, True, True, 6)
        self.pack_start(label_x2, True, True, 6)
        self.pack_start(self.entry_x2, True, True, 6)
        self.pack_start(label_y1, True, True, 6)
        self.pack_start(self.entry_y1, True, True, 6)
        self.pack_start(label_y2, True, True, 6)
        self.pack_start(self.entry_y2, True, True, 6)

    def get_values(self):
        return (self.entry_x1.get_text(), self.entry_x2.get_text(),
                self.entry_y1.get_text(), self.entry_y2.get_text())


class Signature_Position_Dialog(Gtk.Dialog):
    """A dialog box to choose where on the page to sign."""

    def __init__(self, selection, window):
        super().__init__(
            title=_("Signature position:"),
            parent=window,
            flags=Gtk.DialogFlags.MODAL,
            buttons=(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                     Gtk.STOCK_OK, Gtk.ResponseType.OK),
        )
        self.selection = selection
        self.position_widget = _Position_Widget()
        self.vbox.pack_start(self.position_widget, True, True, 6)
        self.show_all()
        self.set_default_response(Gtk.ResponseType.OK)

    def run_get(self):
        result = self.run()
        r = None
        if result == Gtk.ResponseType.OK:
            r = self.position_widget.get_values()
        self.destroy()
        return r


def sign_pdf(filename):
    print('Not siging for now!' + filename)
    pkcs11_lib = '/usr/lib/x86_64-linux-gnu/pkcs11/beidpkcs11.so'

    from pyhanko.sign.beid import open_beid_session, BEIDSigner
    from pyhanko.sign import signers
    from pyhanko.sign.fields import SigFieldSpec
    from pyhanko.pdf_utils.incremental_writer import IncrementalPdfFileWriter
    eidsession = open_beid_session(pkcs11_lib)
    eidsigner = BEIDSigner(eidsession, use_auth_cert=False)

    w = IncrementalPdfFileWriter(open(filename, 'rb+'))
    signers.PdfSigner(
            signers.PdfSignatureMetadata(field_name='Signature1'),
            signer=eidsigner,
            new_field_spec=SigFieldSpec(sig_field_name='Signature1',
                                        on_page=0,
                                        box=(75, 250, 175, 285))
            ).sign_pdf(w, in_place=True)
    # w.write_in_place()
