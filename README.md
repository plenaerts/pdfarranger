## PDFSign fork
This is a fork of https://github.com/pdfarranger/pdfarranger to work on PKCS11 signatures on PDF files. My goal is to let [my Belgian e-ID card](https://eid.belgium.be/nl) put legally valid, eIDAS compliant signatures with a visual stamp on the pdf using a GUI tool. If you know of a tool which can do this without technical fiddling today in Linux, let me know.

I chose to do this in pdfarranger because it was the PDF tool of which I understood parts of the code that I needed to extend quickest.

We'll be doing the signature stuff using https://github.com/MatthiasValvekens/pyHanko/. I've been using pyhanko a couple of times from command line. It works very well, but it's a drag to hit and miss the coordinates for the stamp. Hence my attempt at something.

Consider all of the code in my fork as WIP. Not working. Not even alfa. My ambition probably does not reach all the features one would think of for digital signatures on PDF's, but don't hesitate to look at it and advise me on how to do better.

