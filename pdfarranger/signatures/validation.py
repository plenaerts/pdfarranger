import gettext
from gi.repository import Gtk

_ = gettext.gettext


class SigValidationDialog(Gtk.Dialog):
    """A dialog box to show signature validation info."""

    def __init__(self, filename, window):
        super().__init__(
                title=_("Signature validation:"),
                parent=window,
                flags=Gtk.DialogFlags.MODAL,
                buttons=(Gtk.STOCK_OK, Gtk.ResponseType.OK),
                )

        from pyhanko.sign.general import load_cert_from_pemder
        from pyhanko_certvalidator import ValidationContext
        from pyhanko.pdf_utils.reader import PdfFileReader
        from pyhanko.sign.validation import validate_pdf_signature

#        root_cert = load_cert_from_pemder('path/to/certfile')
#        vc = ValidationContext(trust_roots=[root_cert])
        filename = '/home/pieter/Documenten/sign_test2.pdf'
        with open(filename, 'rb') as doc:
            r = PdfFileReader(doc)
            sig = r.embedded_signatures[0]
            status = validate_pdf_signature(sig)  # , vc)
        textview = Gtk.TextView()
        textview.set_editable(False)
        textview.get_buffer().set_text(status.pretty_print_details())
        self.vbox.pack_start(textview, True, True, 6)
        self.show_all()
        self.set_default_response(Gtk.ResponseType.OK)

class SignedPDFChooser(Gtk.FileChooserDialog):
    def __init__(self, window):
        super().__init__(
            title="Choose a signed PDF file:",
            parent=window,
            action=Gtk.FileChooserAction.OPEN)
        self.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN,
            Gtk.ResponseType.OK)
        filter_pdf = Gtk.FileFilter()
        filter_pdf.set_name("PDF files")
        filter_pdf.add_mime_type("application/pdf")
        self.add_filter(filter_pdf)