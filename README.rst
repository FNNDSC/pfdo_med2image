pfdo_med2image 1.1.24
=====================

.. image:: https://badge.fury.io/py/pfdo_med2image.svg
    :target: https://badge.fury.io/py/pfdo_med2image

.. image:: https://travis-ci.org/FNNDSC/pfdo_med2image.svg?branch=master
    :target: https://travis-ci.org/FNNDSC/pfdo_med2image

.. image:: https://img.shields.io/badge/python-3.5%2B-blue.svg
    :target: https://badge.fury.io/py/pfdo_med2image

.. contents:: Table of Contents


Quick Overview
--------------

-  ``pfdo_med2image`` demonstrates how to use ``pftree`` to transverse directory trees and execute a ``med2image`` analysis at each directory level (that optionally contains files of interest).

Overview
--------

``pfdo_med2image`` leverages the ``pfree`` callback coding contract to target a specific directory with specific files in an arbitrary file tree. At each target directory, an appropriate ``med2image`` call is executed on the files contents at that nested target directory.

For example, imagine a nested tree of ``NIfTI`` image files that need to be converted to ``JPG`` in an output directory tree that preserves the structure of the input tree. In such a case, ``pfdo_med2image`` is a useful tool since it connects ``med2image`` to the ``pftree`` processing machinery.

Installation
------------

Dependencies
~~~~~~~~~~~~

The following dependencies are installed on your host system/python3 virtual env (they will also be automatically installed if pulled from pypi):

-  ``pfmisc`` (various misc modules and classes for the pf* family of objects)
-  ``pftree`` (create a dictionary representation of a filesystem hierarchy)
-  ``pfdo``   (the base module that does the core interfacing with ``pftree``)

Using ``PyPI``
~~~~~~~~~~~~~~

The best method of installing this script and all of its dependencies is
by fetching it from PyPI

.. code:: bash

        pip3 install pfdo_med2image

Command line arguments
----------------------

.. code:: html


        -I|--inputDir <inputDir>
        Input base directory to traverse.

        -O|--outputDir <outputDir>
        The output root directory that will contain a tree structure identical
        to the input directory, and each "leaf" node will contain the analysis
        results.

        [-i|--inputFile <inputFile>]
        An optional <inputFile> specified relative to the <inputDir>. If
        specified, then do not perform a directory walk, but convert only
        this file.

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

        [--fileFilter <someFilter1,someFilter2,...>]
        An optional comma-delimated string to filter out files of interest
        from the <inputDir> tree. Each token in the expression is applied in
        turn over the space of files in a directory location, and only files
        that contain this token string in their filename are preserved.

        [-d|--dirFilter <someFilter1,someFilter2,...>]
        An additional filter that will further limit any files to process to
        only those files that exist in leaf directory nodes that have some
        substring of each of the comma separated <someFilter> in their
        directory name.

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

        [--outputLeafDir <outputLeafDirFormat>]
        If specified, will apply the <outputLeafDirFormat> to the output
        directories containing data. This is useful to blanket describe
        final output directories with some descriptive text, such as
        'anon' or 'preview'.

        This is a formatting spec, so

            --outputLeafDir 'preview-%%s'

        where %%s is the original leaf directory node, will prefix each
        final directory containing output with the text 'preview-' which
        can be useful in describing some features of the output set.

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
        <3DbinVector>

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

        [--threads <numThreads>]
        If specified, break the innermost analysis loop into <numThreads>
        threads.

        [-x|--man]
        Show full help.

        [-y|--synopsis]
        Show brief help.

        [--json]
        If specified, output a JSON dump of final return.

        [--followLinks]
        If specified, follow symbolic links.

        -v|--verbosity <level>
        Set the app verbosity level.

            0: No internal output;
            1: Run start / stop output notification;
            2: As with level '1' but with simpleProgress bar in 'pftree';
            3: As with level '2' but with list of input dirs/files in 'pftree';
            5: As with level '3' but with explicit file logging for
                    - read
                    - analyze
                    - write

Examples
--------

NIfTI to jpg
~~~~~~~~~~~~

Run down a directory tree and process all the files in the input tree that are ``nii``, converting them to ``jpg`` at corresponding locations in the output directory:

.. code:: bash

        pfdo_med2image                                      \
            -I /var/www/html/data --fileFilter nii          \
            -O /var/www/html/jpg                            \
            -t jpg                                          \
            --threads 0 --printElapsedTime


The above will find all files in the tree structure rooted at /var/www/html/data that also contain the string "nii" anywhere in the filename. For each file found, a `med2image` conversion will be called in the output directory, in the same tree location as the original input.

Convert a nested tree of DICOMs:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Since ``med2image`` will by default attempt to convert all DICOMS in a directory, we only need to "tag" a single DICOM in a given directory to convert:

.. code:: bash

        pfdo_med2image                                      \
            -I /home/rudolph/src/pl-dcm2img/in              \
            -O $PWD/out                                     \
            --analyzeFileIndex f                            \
            --fileFilter dcm -t jpg                         \
            --threads 0 --printElapsedTime

The initial ``--fileFilter dcm`` will tag only dirs/files that contain ``dcm`` in their filename strings while the additional ``--analyzeFileIndex f`` will ultimately only call call ``med2image`` **once**. When called, ``med2image`` will self-discover and covert all files in each working directory. Pedantically, an equivalent, but slower call:

Pedantically, an equivalent, but slower approach that calls a separate ``med2image`` on **each** tagged DICOM input:

.. code:: bash

        pfdo_med2image                                      \
            -I /home/rudolph/src/pl-dcm2img/in              \
            -O $PWD/out                                     \
            --convertOnlySingleDICOM                        \
            --fileFilter dcm -t jpg                         \
            --threads 0 --printElapsedTime

Finally the elapsed time is also printed.

