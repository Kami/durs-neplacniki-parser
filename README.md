# DURS Neplacniki Parser

Slovenian government published a list of non-paying taxpayers on the tax
administration of the republic of Slovenia website in non-machine readable
format. The list consists of a bunch of HTML files with embedded images.

Utilities in this repository allow you to convert this list to raw text files so
it's easier to view it.

## Dependencies

* Python
* Python dependencies (`pip install -r requirements.txt`)
* Imagemagick - for scaling and optimizing images to make them easier to OCR
* tesseract - for OCR-ing the images
* tesseract Slovenian language data - https://code.google.com/p/tesseract-ocr/downloads/detail?name=slv.traineddata.gz
