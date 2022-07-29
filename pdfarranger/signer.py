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
            r = min(self.selection).get_indices()[0]
        elif result == 2:
            r = max(self.selection).get_indices()[0]
        elif result == Gtk.ResponseType.CANCEL:
            r = None
        self.destroy()
        return r


class _Coords_Icon_Window(Gtk.ScrolledWindow):
    def __init__(self, page_selection):
        super().__init__()
        self.page_selection = page_selection
        self.connect('drag_data_received', self.sw_dnd_received_data)
        self.connect('button_press_event', self.sw_button_press_event)
        self.connect('scroll_event', self.sw_scroll_event)
        self.add(Gtk.Label('A label!'))
        self.show_all()

    def sw_dnd_received_data(self):
        print('Drag and drop not implemented yet.')

    def sw_button_press_event(self):
        print('Button press not implemented yet.')

    def sw_scroll_event(self):
        print('Scroll event not implemented yet.')


class _Coords_Widget(Gtk.HBox):
    """A form to specify the coords of the position of the
    signature on a page."""

    def __init__(self, page_icon):
        super().__init__()
        # So, here we should show another dialog with an image.
        # We want the user to click that image in some place, and get the
        # coords.
        label_x1 = Gtk.Label(label="x1:")
        label_x2 = Gtk.Label(label="x2:")
        label_y1 = Gtk.Label(label="y1:")
        label_y2 = Gtk.Label(label="y2:")
        self.entry_x1 = Gtk.Entry(text="75", width_chars=3)
        self.entry_x2 = Gtk.Entry(text="225", width_chars=3)
        self.entry_y1 = Gtk.Entry(text="100", width_chars=3)
        self.entry_y2 = Gtk.Entry(text="25", width_chars=3)
        self.pack_start(label_x1, True, True, 6)
        self.pack_start(self.entry_x1, True, True, 6)
        self.pack_start(label_x2, True, True, 6)
        self.pack_start(self.entry_x2, True, True, 6)
        self.pack_start(label_y1, True, True, 6)
        self.pack_start(self.entry_y1, True, True, 6)
        self.pack_start(label_y2, True, True, 6)
        self.pack_start(self.entry_y2, True, True, 6)

    def get_coords(self):
        coords = (float(self.entry_x1.get_text()),
                  float(self.entry_y1.get_text()),
                  float(self.entry_x2.get_text()),
                  float(self.entry_y2.get_text()))
        return coords


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
        self.coords_icon_window = _Coords_Icon_Window(selection)
        self.vbox.pack_start(self.coords_icon_window, True, True, 6)
        self.coords_widget = _Coords_Widget(self.selection)
        self.vbox.pack_start(self.coords_widget, True, True, 6)
        self.show_all()
        self.set_default_response(Gtk.ResponseType.OK)

    def run_get(self):
        result = self.run()
        r = None
        if result == Gtk.ResponseType.OK:
            r = self.coords_widget.get_coords()
        self.destroy()
        return r


def sign_pdf(filename, sign_page, sign_coords):
    # TODO: this should become configurable
    pkcs11_lib = '/usr/lib/x86_64-linux-gnu/pkcs11/beidpkcs11.so'

    # TODO: we should move this to an earlier point.
    # Without pyhanko we should not show the sign action.
    from pyhanko.sign.beid import open_beid_session, BEIDSigner
    from pyhanko.sign import signers
    from pyhanko.sign.fields import SigFieldSpec
    from pyhanko.pdf_utils.incremental_writer import IncrementalPdfFileWriter

    eidsession = open_beid_session(pkcs11_lib)
    eidsigner = BEIDSigner(eidsession, use_auth_cert=False)

    w = IncrementalPdfFileWriter(open(filename, 'rb+'))

    # Some debugging stuff. Should use logging?
    msg = 'Signing with coords: ' + str(sign_coords) + ' with types: ' + \
          str(type(sign_coords)) + ' holding '
    for sc in sign_coords:
        msg.append(str(type(sc)))
    print(msg)

    signers.PdfSigner(
            signers.PdfSignatureMetadata(field_name='Signature1'),
            signer=eidsigner,
            new_field_spec=SigFieldSpec(sig_field_name='Signature1',
                                        on_page=sign_page,
                                        box=sign_coords)
            ).sign_pdf(w, in_place=True)
