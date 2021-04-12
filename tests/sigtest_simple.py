"""
Sign a pdf using pyhanko's API.

Ref
https://pyhanko.readthedocs.io/en/latest/lib-guide/signing.html#a-simple-example
https://pyhanko.readthedocs.io/en/latest/lib-guide/sig-fields.html
"""

from pyhanko.sign import signers
from pyhanko.sign import beid
from pyhanko.sign.fields import SigFieldSpec
from pyhanko.pdf_utils.incremental_writer import IncrementalPdfFileWriter
import argparse

parser = argparse.ArgumentParser(description='Do some BE E-ID test on a PDF.')
parser.add_argument('infile', type=argparse.FileType('rb'),
                    help='input file to sign. Won\'t be changed.')
parser.add_argument('outfile', type=argparse.FileType('wb'),
                    help='outfile to write the input PDF to.')
parser.add_argument('--pkcs11_lib', default='/usr/lib/x86_64-linux-gnu/pkcs11/beidpkcs11.so',
                    help='pkcs11 library to use. Best try the BE EID pkcs11 lib. Not tested with others.')

args = parser.parse_args()

eidsession = beid.open_beid_session(args.pkcs11_lib)
eidsigner = beid.BEIDSigner(eidsession, use_auth_cert=False)

infile = args.infile
outfile = args.outfile

w = IncrementalPdfFileWriter(infile)
out = signers.PdfSigner(
    signers.PdfSignatureMetadata(field_name='Signature1'),
    signer=eidsigner,
    new_field_spec=SigFieldSpec(sig_field_name='Signature1',
                                on_page=0,
                                box=(75, 250, 175, 285))
).sign_pdf(w)

outfile.write(out.read())
outfile.close()
infile.close()
