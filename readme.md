# mactime.py
## Description
mactime.py is a tool that takes a [bodyfile](https://wiki.sleuthkit.org/index.php?title=Body_file) formatted export of a devices MFT and converts it to the [mactime format](https://wiki.sleuthkit.org/index.php?title=Mactime_output) created by Sleuthkit's mactime.pl. 

## Syntax
    usage: mactime.py [-h] -f BODY_FILE -o OUTFILE

    mactime is a tool that will convert the standard bodyfile format into a mactime formatted timeline (as csv).

    options:
    -h, --help    show this help message and exit
    -f BODY_FILE  Bodyfile to process. (default: None)
    -o OUTFILE    File to save the output results to. (default: None)

    v1.0.0 | Author: Stephen Hurd | @HurdDFIR

