pfdo_med2image 1.1.6
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

        [--dirFilter <someFilter1,someFilter2,...>]
        Similar to the `fileFilter` but applied over the space of leaf node
        in directory paths. A directory must contain at least one file
        to be considered.

        If a directory leaf node contains a string that corresponds to any of
        the filter tokens, a special "hit" is recorded in the file hit list,
        "%d-<leafnode>". For example, a directory of

                            /some/dir/in/the/inputspace/here1234

        with a `dirFilter` of `1234` will create a "special" hit entry of
        "%d-here1234" to tag this directory for processing.

        In addition, if a directory is filtered through, all the files in
        that directory will be added to the filtered file list. If no files
        are to be added, passing an explicit file filter with an "empty"
        single string argument, i.e. `--fileFilter " "`, is advised.

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

        [--func <functionName>]
        Apply the specified transformation function before saving. Currently
        support functions:

            * invertIntensities
              Inverts the contrast intensity of the source image.

        [--reslice]
        For 3D data only. Assuming [i,j,k] coordinates, the default is to save
        along the 'k' direction. By passing a --reslice image data in the 'i' and
        'j' directions are also saved. Furthermore, the <outputDir> is subdivided into
        'slice' (k), 'row' (i), and 'col' (j) subdirectories.

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

Run down a directory tree and process all the files in the input tree that are ``nii``, converting them to ``jpg`` at corresponding locations in the output directory:

.. code:: bash

        pfdo_med2image                                      \
            -I /var/www/html/data --filter nii              \
            -O /var/www/html/jpg                            \
            -t jpg                                          \
            --threads 0 --printElapsedTime


The above will find all files in the tree structure rooted at /var/www/html/data that also contain the string "nii" anywhere in the filename. For each file found, a `med2image` conversion will be called in the output directory, in the same tree location as the original input.

Finally the elapsed time and a JSON output are printed.

