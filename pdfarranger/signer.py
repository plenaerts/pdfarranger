import gettext
from gi.repository import Gtk

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


class _Coords_Widget(Gtk.Grid):
    """A grid to specify the coords of the position of the
    signature on a page."""

    def __init__(self, page_icon):
        super().__init__()
        # We want the user to click that image in some place, and get the
        # coords. Now the user must enter coord numbers and guess until
        # the rectangle position seems about right on a white background...

        self.set_column_homogeneous(True)
        self.set_row_homogeneous(False)

        self.darea = Gtk.DrawingArea()
        self.darea.set_hexpand(True)
        self.darea.set_vexpand(True)
        self.darea.set_halign(Gtk.Align.FILL)
        self.darea.set_valign(Gtk.Align.FILL)
        self.darea.connect('draw', self.on_draw)
        self.attach(self.darea, 0, 0, 8, 1)

        label_x1 = Gtk.Label(label="x1:")
        label_x2 = Gtk.Label(label="x2:")
        label_y1 = Gtk.Label(label="y1:")
        label_y2 = Gtk.Label(label="y2:")
        self.entry_x1 = Gtk.Entry(text="75", width_chars=3)
        self.entry_x2 = Gtk.Entry(text="225", width_chars=3)
        self.entry_y1 = Gtk.Entry(text="25", width_chars=3)
        self.entry_y2 = Gtk.Entry(text="100", width_chars=3)
        self.entry_x1.connect('changed', self.refresh_preview)
        self.entry_x2.connect('changed', self.refresh_preview)
        self.entry_y1.connect('changed', self.refresh_preview)
        self.entry_y2.connect('changed', self.refresh_preview)
        self.attach(label_x1, 0, 1, 1, 1)
        self.attach(self.entry_x1, 1, 1, 1, 1)
        self.attach(label_x2, 2, 1, 1, 1)
        self.attach(self.entry_x2, 3, 1, 1, 1)
        self.attach(label_y1, 4, 1, 1, 1)
        self.attach(self.entry_y1, 5, 1, 1, 1)
        self.attach(label_y2, 6, 1, 1, 1)
        self.attach(self.entry_y2, 7, 1, 1, 1)

    def refresh_preview(self, widget):
        self.darea.queue_draw()

    def on_draw(self, widget, event):
        height = widget.get_allocated_height()
        width = widget.get_allocated_width()
        # page_ratio = self.PAGE_HEIGHT / self.PAGE_WIDTH
        cr = widget.get_window().cairo_create()
        # A white background.
        cr.set_source_rgb(1, 1, 1)
        page_offset_left = round((width - 210) / 2)
        page_offset_top = round((height - 297)/2)
        cr.rectangle(page_offset_left, page_offset_top, 210, 297)
        cr.fill()
        # A black outline for the white background.
        cr.set_line_width(1)
        cr.set_source_rgb(0, 0, 0)
        cr.rectangle(page_offset_left, page_offset_top, 210, 297)
        cr.stroke()
        # The signature field in red.
        cr.set_line_width(1)
        cr.set_source_rgb(1, 0, 0)

        # PDF's use 72 DPI Cartesian coords = 0,0 is bottom left of page.
        # Cairo's coord system works top left to bottom right.
        # We take mm to pixels for convenience to display a rectangle for
        # a page. That means we should divide each PDF coordinate by
        # DP_MM = Dots Per MM, with 1 inch being 25.4 mm.

        DPI = 72.0  # 72 coord points in the PDF coord system = 1 inch
        DP_MM = DPI / 25.4  # 1 Inch = 25,4 Millimeter

        # origin_x is the x value of the left side of the page in cairo.
        origin_x = page_offset_left
        # origin_y is the y value of the bottom of the page in cairo.
        origin_y = page_offset_top + 297

        # sig_x1 is the left edge of the signature. It should be to the
        # right of the left side of the page in cairo, that means adding.
        sig_x1 = round(float(self.entry_x1.get_text()) / DP_MM) + \
            origin_x
        # sig_width is the width of the signature = the difference between
        # the X values.
        sig_width = round(float(self.entry_x2.get_text()) / DP_MM) - \
            round(float(self.entry_x1.get_text()) / DP_MM)

        # sig_y1 is top of the signature. It should be above the page bottom
        # in cairo, that means subtracting.
        sig_y1 = origin_y - round(float(self.entry_y2.get_text()) / DP_MM)
        # sig_height is the height of the signature = the difference between
        # the Y values.
        sig_height = round(float(self.entry_y2.get_text()) / DP_MM) - \
            round(float(self.entry_y1.get_text()) / DP_MM)

        cr.rectangle(sig_x1, sig_y1, sig_width, sig_height)
        cr.fill()

    def get_coords(self):
        """Get the contents from the PDF Cartesian coordinates
        entry fields as a tuple of four floats: (x1, y1, x2, y2).
        """
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
        self.set_default_size(300, 500)
        self.selection = selection
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
        msg = msg + str(type(sc))
    print(msg)

    signers.PdfSigner(
            signers.PdfSignatureMetadata(field_name='Signature1'),
            signer=eidsigner,
            new_field_spec=SigFieldSpec(sig_field_name='Signature1',
                                        on_page=sign_page,
                                        box=sign_coords)
            ).sign_pdf(w, in_place=True)
