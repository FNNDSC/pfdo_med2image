#!/usr/bin/env python3
#
# (c) 2020 Fetal-Neonatal Neuroimaging & Developmental Science Center
#                   Boston Children's Hospital
#
#              http://childrenshospital.org/FNNDSC/
#                        dev@babyMRI.org
#

import sys, os
sys.path.insert(1, os.path.join(os.path.dirname(__file__), '../pfdo_med2image'))

# Turn off all logging for modules in this libary.
import logging
logging.disable(logging.CRITICAL)

import  pfdo.__main__       as pfdo_main
import  pfdo
try:
    from    .               import pfdo_med2image
    from    .               import __pkg, __version__
except:
    from pfdo_med2image     import pfdo_med2image
    from __init__           import __pkg, __version__

from    argparse            import RawTextHelpFormatter
from    argparse            import ArgumentParser
import  pudb

import  pfmisc
from    pfmisc._colors      import Colors
from    pfmisc              import other

str_desc = Colors.CYAN + """

        __    _                           _  _____  _
       / _|  | |                         | |/ __  \(_)
 _ __ | |_ __| | ___   _ __ ___   ___  __| |`' / /' _ _ __ ___   __ _  __ _  ___
| '_ \|  _/ _` |/ _ \ | '_ ` _ \ / _ \/ _` |  / /  | | '_ ` _ \ / _` |/ _` |/ _ \
| |_) | || (_| | (_) || | | | | |  __/ (_| |./ /___| | | | | | | (_| | (_| |  __/
| .__/|_| \__,_|\___/ |_| |_| |_|\___|\__,_|\_____/|_|_| |_| |_|\__,_|\__, |\___|
| |               ______                                               __/ |
|_|              |______|                                             |___/



                          Path-File Do med2image

        Recursively walk down a directory tree and perform a 'med2image'
        on files in each directory (optionally filtered by some simple
        expression). Results of each operation are saved in output tree
        that  preserves the input directory structure.


                             -- version """ + \
             Colors.YELLOW + __version__ + Colors.CYAN + """ --

        'pfdo_med2image' demonstrates how to use ``pftree`` to transverse
        directory trees and execute a ``med2image`` analysis at each directory
        level (that optionally contains files of interest).

        As part of the "pf*" suite of applications, it is geared to IO as
        directories. Nested directory trees within some input directory
        are reconstructed in an output directory, preserving directory
        structure.


""" + Colors.NO_COLOUR

package_CLI = '''
        [-t|--outputFileType <outputFileType>]              \\
        [-s|--sliceToConvert <sliceToConvert>]              \\
        [--convertOnlySingleDICOM]                          \\
        [--preserveDICOMinputName]                          \\
        [-f|--frameToConvert <frameToConvert>]              \\
        [--showSlices]                                      \\
        [--func <functionName>]                             \\
        [--reslice]                                         \\
        [--rotAngle <angle>]                                \\
        [--rot <3vec>]                                      \\''' + \
        pfdo_main.package_CLI

package_argSynopsis = pfdo_main.package_argSynopsis + '''
        [--inputFileSubStr <substr>]
        As a convenience, the input file can be determined via a substring
        search of all the files in the <inputDir> using this flag. The first
        filename hit that contains the <substr> will be assigned the
        <inputFile>.

        This flag is useful is input names are long and cumbersome, but
        a short substring search would identify the file. For example, an
        input file of

           0043-1.3.12.2.1107.5.2.19.45152.2013030808110149471485951.dcm

        can be specified using ``--inputFileSubStr 0043-``

        [--analyzeFileIndex <someIndex>]
        An optional string to control which file(s) in a specific directory
        to which the analysis is applied. The default is "-1" which implies
        *ALL* files in a given directory. Other valid <someIndex> are:
            'm':   only the "middle" file in the returned file list
            "f":   only the first file in the returned file list
            "l":   only the last file in the returned file list
            "<N>": the file at index N in the file list. If this index
                   is out of bounds, no analysis is performed.
            "-1" means all files.

        [-o|--outputFileStem <outputFileStem>]
        The output file stem to store conversion. If this is specified
        with an extension, this extension will be used to specify the
        output file type.

        SPECIAL CASES:
        For DICOM data, the <outputFileStem> can be set to the value of
        an internal DICOM tag. The tag is specified by preceding the tag
        name with a percent character '%%', so

            -o %%ProtocolName

        will use the DICOM 'ProtocolName' to name the output file. Note
        that special characters (like spaces) in the DICOM value are
        replaced by underscores '_'.

        Multiple tags can be specified, for example

            -o %%PatientName%%PatientID%%ProtocolName

        and the output filename will have each DICOM tag string as
        specified in order, connected with dashes.

        [--convertOnlySingleDICOM]
        If specified, will only convert the single DICOM specified by the
        '--inputFile' flag. This is useful for the case when an input
        directory has many DICOMS but you specifially only want to convert
        the named file. By default the script assumes that multiple DICOMS
        should be converted en mass otherwise.

        [--preserveDICOMinputName]
        If specified, use the input DICOM name as the base of the output
        filename.

        [-t|--outputFileType <outputFileType>]
        The output file type. If different to <outputFileStem> extension,
        will override extension in favour of <outputFileType>.

        [-s|--sliceToConvert <sliceToConvert>]
        In the case of volume files, the slice (z) index to convert. Ignored
        for 2D input data. If a '-1' is sent, then convert *all* the slices.
        If an 'm' is specified, only convert the middle slice in an input
        volume.

        [-f|--frameToConvert <sliceToConvert>]
        In the case of 4D volume files, the volume (V) containing the
        slice (z) index to convert. Ignored for 3D input data. If a '-1' is
        sent, then convert *all* the frames. If an 'm' is specified, only
        convert the middle frame in the 4D input stack.

        [--showSlices]
        If specified, render/show image slices as they are created.

        [--rot <3DbinVector>]
        A per dimension binary rotation vector. Useful to rotate individual
        dimensions by an angle specified with [--rotAngle <angle>]. Default
        is '110', i.e. rotate 'x' and 'y' but not 'z'. Note that for a
        non-reslice selection, only the 'z' (or third) element of the vector
        is used.

        [--rotAngle <angle>]
        Default 90 -- the rotation angle to apply to a given dimension of the
        <3DbinVector>.

        [--func <functionName>]
        Apply the specified transformation function before saving. Currently
        support functions:

            * invertIntensities
              Inverts the contrast intensity of the source image.

        [--reslice]
        For 3D data only. Assuming [x,y,z] coordinates, the default is to save
        along the 'z' direction. By passing a --reslice image data in the 'x'
        and 'y' directions are also saved. Furthermore, the <outputDir> is
        subdivided into 'slice' (z), 'row' (x), and 'col' (y) subdirectories.

'''

def synopsis(ab_shortOnly = False):
    scriptName = os.path.basename(sys.argv[0])
    shortSynopsis =  """
    NAME

        pfdo_med2image

    SYNOPSIS

        pfdo_med2image """ + package_CLI + """

    BRIEF EXAMPLE

        pfdo_med2image                                      \\
            -I /var/www/html/data --fileFilter nii          \\
            -O /var/www/html/jpg                            \\
            -t jpg                                          \\
            --threads 0 --printElapsedTime
    """

    description =  '''
    DESCRIPTION

        ``pfdo_med2image`` runs ``med2image`` at each path/file location in an
        input tree. The CLI space is the union of ``pfdo`` and ``med2image``.

    ARGS ''' + package_argSynopsis + '''

    EXAMPLES

    Perform a `pfdo_med2image` down some input directory:
    -----------------------------------------------------

        pfdo_med2image                                      \\
            -I /var/www/html/data --fileFilter nii          \\
            -O /var/www/html/jpg                            \\
            -t jpg                                          \\
            --threads 0 --printElapsedTime

    The above will find all files in the tree structure rooted at
    /var/www/html/data that also contain the string "nii" anywhere
    in the filename. For each file found, a `med2image` conversion
    will be called in the output directory, in the same tree location as
    the original input.

    Convert a nested tree of DICOMs:
    --------------------------------

    Since `med2image` will by default attempt to convert all DICOMS
    in a directory, we only need to "tag" a single DICOM in a given
    directory to convert:

        pfdo_med2image                                      \\
            -I /home/rudolph/src/pl-dcm2img/in              \\
            -O $PWD/out                                     \\
            --analyzeFileIndex f                            \\
            --fileFilter dcm -t jpg                         \\
            --threads 0 --printElapsedTime

    The initial `--fileFilter dcm` will tag only dirs/files that
    contain `dcm` in their filename strings while the additional
    `--analyzeFileIndex f` instructs ``pfdo_med2image`` to only
    call ``med2image`` **once**. When called, ``med2image`` will
    self-discover and covert all files in each working directory.

    Pedantically, an equivalent, but slower approach that calls
    a separate ``med2image`` on **each** tagged DICOM input:

        pfdo_med2image                                      \\
            -I /home/rudolph/src/pl-dcm2img/in              \\
            -O $PWD/out                                     \\
            --convertOnlySingleDICOM                        \\
            --fileFilter dcm -t jpg                         \\
            --threads 0 --printElapsedTime

    Finally the elapsed time is also printed.

    '''

    if ab_shortOnly:
        return shortSynopsis
    else:
        return shortSynopsis + description


parser              = pfdo_main.parser
parser.description  = str_desc

parser.add_argument("--analyzeFileIndex",
                    help    = "file index per directory to analyze",
                    dest    = 'analyzeFileIndex',
                    default = '-1')

# med2image additional CLI flags
parser.add_argument("-o", "--outputFileStem",
                    help    = "output file",
                    default = "output.jpg",
                    dest    = 'outputFileStem')
parser.add_argument("-t", "--outputFileType",
                    help    = "output image type",
                    dest    = 'outputFileType',
                    default = '')
parser.add_argument("--convertOnlySingleDICOM",
                    help    = "if specified, only convert the specific input DICOM",
                    dest    = 'convertOnlySingleDICOM',
                    action  = 'store_true',
                    default = False)
parser.add_argument("--preserveDICOMinputName",
                    help    = "if specified, save output files with the basename of their input DICOM",
                    dest    = 'preserveDICOMinputName',
                    action  = 'store_true',
                    default = False)
parser.add_argument("-s", "--sliceToConvert",
                    help="slice to convert (for 3D data)",
                    dest='sliceToConvert',
                    default='-1')
parser.add_argument("--frameToConvert",
                    help    = "frame to convert (for 4D data)",
                    dest    = 'frameToConvert',
                    default = '-1')
parser.add_argument('-r', '--reslice',
                    help    = "save images along i,j,k directions -- 3D input only",
                    dest    = 'reslice',
                    action  = 'store_true',
                    default = False)
parser.add_argument('--showSlices',
                    help    = "show slices that are converted",
                    dest    = 'showSlices',
                    action  = 'store_true',
                    default = False)
parser.add_argument('--func',
                    help    = "apply transformation function before saving",
                    dest    = 'func',
                    default = "")
parser.add_argument('--rot',
                    help    = "3D slice/dimenstion rotation vector",
                    dest    = 'rot',
                    default = "110")
parser.add_argument('--rotAngle',
                    help    = "3D slice/dimenstion rotation angle",
                    dest    = 'rotAngle',
                    default = "90")


def main(argv = None):
    args = parser.parse_args()
    pudb.set_trace()
    if args.man or args.synopsis:
        print(str_desc)
        if args.man:
            str_help     = synopsis(False)
        else:
            str_help     = synopsis(True)
        print(str_help)
        sys.exit(1)

    if args.b_version:
        print("Name:    %s\nVersion: %s" % (__pkg.name, __version__))
        sys.exit(1)

    args.str_version    = __version__
    args.str_desc       = synopsis(True)

    pf_do_med2image     = pfdo_med2image.pfdo_med2image(vars(args))

    # And now run it!
    d_pfdo_med2image    = pf_do_med2image.run(timerStart = True)

    if args.printElapsedTime:
        pf_do_med2image.dp.qprint(
                "Elapsed time = %f seconds" %
                d_pfdo_med2image['runTime']
        )

    sys.exit(0)

if __name__ == "__main__":
    sys.exit(main())