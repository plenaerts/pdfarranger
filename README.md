# PDFSign fork of PDF Arranger

This is a fork of https://github.com/pdfarranger/pdfarranger to sign PDF documents using https://github.com/MatthiasValvekens/pyHanko/.

This fork is currently usable for me. **Any errors you encounter are welcome as issues!**

## Installation
The easiest way to start using this fork is installing the prerequisites, cloning this repository and installing the python package in [a python virtual environment](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/).

### Prerequisites
Following software is required: git, build-essential, python3 (Ubuntu: python3-dev, python3-venv, python3-wheel, python3-distutils-extra, python3-cairo), gir1.2-poppler-0.18 and eid-mw from [the Belgian eID middleware](https://eid.belgium.be/nl/linux-eid-software-installatie).

You need an eID card reader as well, working with the eID middleware. Best/easiest is to install the eID middleware and it's eID viewer first and check that the viewer shows the info from your eID card correctly.
 
#### Ubuntu
For Ubuntu desktop and related distro's, probably Debian too, you should install git, python3, python3-distutils-extra using the Ubuntu package manager:

```
sudo apt-get install git python3 python3-dev python3-venv python3-wheel python3-distutils-extra python3-cairo gir1.2-poppler-0.18
```

To install the the Belgian eID middleware:
- Download the eid-archive deb from the [download page](https://eid.belgium.be/nl/linux-eid-software-installatie).
- Install the .deb using ```sudo dpkg -i <downloaded_deb_file>```. This should add the right APT source for Ubuntu's package manager.
- Install the eid-mw and (optionally) eid-viewer packages: ```sudo apt-get install eid-mw eid-viewer```.

#### For other distros
- Install the packages above.
- Currently the eid middleware is expected at ```/usr/lib/x86_64-linux-gnu/pkcs11/beidpkcs11.so```. Hardcoded for the moment in pdfarranger/signer.py.
- GTK is required too. If you are trying this on a system without GTK I assume you know what to do to fix the errors you get.

### Clone and install this PDF Arranger fork in a virtual environment
To avoid littering your system with unmanaged files it is best and easiest to use a python virtual environment to keep the python dependencies for this package managed and isolated. A virtual environment keeps everything in a directory. Placeholder *install_dir* below is this virtual environment directory where PDF Arranger will be installed with its dependencies.

```bash
python3 -m venv <install_dir> --system-site-packages --upgrade-deps
source <install_dir>/bin/activate
pip install "git+https://github.com/plenaerts/pdfarranger.git" "pyhanko[pkcs11,image-support,opentype]"
```

## Usage
### Signing
- Run the python entry-point ```<install_dir>/bin/pdfarranger``` . Double-click it or run it from your terminal.
- Open a PDF.
- Select and right click the page where you want your signature to appear.
- Choose "Sign".
- If you selected multiple pages, choose to sign the first of the last page. (Best is to just select one single page where you want your signature to appear.)
- Choose where your signature should appear on the page. The coordinates are Cartesian, starting from bottom left and work at 72 DPI in most PDF docs. That makes the bottom-left corner of any sheet x = 0, y = 0 and the top-right corner of an A4 sheet about x = 595, y= 841.
- Choose a filename for the PDF with your signature. Make sure your eID card is in your reader. Signing will happen.
- PDF Arranger saves the document and the eid-mw asks for your eID PIN.
### Signature validation
A very basic signature verification function is added in the main menu.

PDF Arranger has a strong focus on manipulating PDF documents. Verifying signatures requires NOT to manipulate them. Therefore the signature validation functionalities don't follow the other "edit" logic in PDF Arranger:
- The menu item for signature validation is always enabled.
- PDF Arranger will always ask to select a PDF document to validate sigantures in.
- PDF Arrager will display pyHanko validation output in a dialog, but will not open the verified file in PDF Arranger.

### Limitations
Using other **pyHanko options** such as custom signature text, images, other signing mechanisms than the Belgian PKCS11 module, etc, etc, ... are currently not supported. I plan on writing up some dialog that lets you tweak some pyHanko options. My focus will be use cases for non-techie, desktop application, office, everyday, ... users. Mainly for smart cards, i.e. PKCS11.

**Signing with multiple signatures** is currently not tested and does not work in a number of scenario's. The signature's field name is currently hardcoded to 'Signature1' for example. These names should be unique.

**Signature validation is very basic.** It doesn't let you tweak the trust chain for the signature validation. It may be an idea to trust all certs in /etc/ssl/certs ?

## Why this fork?

The goal of this fork is to put PKCS11 signatures with [my Belgian e-ID card](https://eid.belgium.be/nl) on documents. These are legally valid, eIDAS compliant signatures with a visual stamp on the PDF using a GUI tool to choose the signature field position on the document. If you know of a tool which can do this without technical fiddling today in Linux, let me know.

I chose to do this in pdfarranger because it was the PDF tool of which I understood parts of the code that I needed to extend quickest.

We'll be doing the signature stuff using https://github.com/MatthiasValvekens/pyHanko/. I've been using pyhanko a couple of times from command line. It works very well, but it's a drag to hit and miss the coordinates for the stamp. Hence my attempt at something.
