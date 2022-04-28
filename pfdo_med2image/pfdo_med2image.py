# System imports
import      os
import      json
import      pathlib
from        argparse            import  Namespace

# Turn off all logging for modules in this libary.
import logging
logging.disable(logging.CRITICAL)

# Project specific imports
import      pfmisc
from        pfmisc._colors      import  Colors
from        pfmisc              import  other
from        pfmisc              import  error

from        med2image           import  med2image
import      pfdo

import      pudb
import      pftree

class pfdo_med2image(pfdo.pfdo):
    """

    A class for navigating down a dir tree and providing
    hooks for some (subclass) analysis

    """

    _dictErr = {
        'outputDirFail'   : {
            'action'        : 'trying to check on the output directory, ',
            'error'         : 'directory not specified. This is a *required* input.',
            'exitCode'      : 1},
        'outputFileExists'   : {
            'action'        : 'attempting to write an output file, ',
            'error'         : 'it seems a file already exists. Please run with --overwrite to force overwrite.',
            'exitCode'      : 2}
        }


    def declare_selfvars(self):
        """
        A block to declare self variables
        """

        #
        # Object desc block
        #
        self.str_desc                   = ''
        self.__name__                   = "pfdo_med2image"

    def __init__(self, *args, **kwargs):
        """
        Constructor for pfdo_med2image.

        This basically just calls the parent constructor and
        adds some child-specific data.
        """

        super().__init__(*args, **kwargs)

        pfdo_med2image.declare_selfvars(self)

    def inputReadCallback(self, *args, **kwargs):
        """
        This method does not actually read in any files, but
        exists to preserve the list of files associated with a
        given input directory.

        By preserving and returning this file list, the next
        callback function in this pipeline is able to receive an
        input path and a list of files in that path.
        """
        str_path        : str       = ''
        l_fileProbed    : list      = []
        b_status        : bool      = True
        filesProbed     : int       = 0

        if len(args):
            at_data         = args[0]
            str_path        = at_data[0]
            l_fileProbed    = at_data[1]

        if not len(l_fileProbed): b_status = False

        return {
            'status':           b_status,
            'l_fileProbed':     l_fileProbed,
            'str_path':         str_path,
            'filesProbed':      filesProbed
        }

    def inputAnalyzeCallback(self, *args, **kwargs):
        """
        Callback stub for doing actual work. Since the `med2image`
        is a mostly stand-apart module, the inputRead and outputWrite
        callbacks are not applicable here, since calling the
        `med2image` module appropriately reads an input and saves
        an output.
        """

        def l_fileToAnalyze_determine(l_fileProbed):
            """
            Return the list of files to process, based on l_fileProbed
            and self.args['analyzeFileIndex']
            """

            def middleIndex_find(l_lst):
                """
                Return the middle index in a list.
                If list has no length, return None.
                """
                middleIndex     = None
                if len(l_lst):
                    if len(l_lst) == 1:
                        middleIndex = 0
                    else:
                        middleIndex = round(len(l_lst)/2+0.01)
                return middleIndex

            def nIndex_find(l_lst, str_index):
                """
                For a string index, say "2", return the index at l_lst[2].
                If index is out of bounds return None.
                """
                index:  int = 0
                try:
                    index   = int(str_index)
                    if len(l_lst):
                        if index >= -1 and index < len(l_lst):
                            return index
                except:
                    pass
                return None

            l_fileToAnalyze:    list    = []
            if len(l_fileProbed):
                if self.args['analyzeFileIndex'] == 'f': l_fileToAnalyze.append(l_fileProbed[0])
                if self.args['analyzeFileIndex'] == 'l': l_fileToAnalyze.append(l_fileProbed[-1])
                if self.args['analyzeFileIndex'] == 'm':
                    if middleIndex_find(l_fileProbed) >= 0:
                        self.dp.qprint(l_fileProbed, level = 5)
                        l_fileToAnalyze.append(l_fileProbed[middleIndex_find(l_fileProbed)])
                nIndex  = nIndex_find(l_fileProbed, self.args['analyzeFileIndex'])
                if nIndex:
                    if nIndex == -1:
                        l_fileToAnalyze = l_fileProbed
                    else:
                        l_fileToAnalyze.append(nIndex)
            return l_fileToAnalyze

        b_status            : bool  = False
        l_fileProbed        : list  = []
        d_inputReadCallback : dict  = {}
        d_convert           : dict  = {}

        for k, v in kwargs.items():
            if k == 'path':         str_path    = v

        if len(args):
            at_data             = args[0]
            str_path            = at_data[0]
            d_inputReadCallback = at_data[1]
            l_fileProbed        = d_inputReadCallback['l_fileProbed']

        # pudb.set_trace()
        med2image_args                  = self.args.copy()
        for str_file in l_fileToAnalyze_determine(l_fileProbed):
            med2image_args['inputDir']      = str_path
            med2image_args['inputFile']     = str_file
            med2image_args['outputDir']     = str_path.replace(
                                                self.args['inputDir'],
                                                self.args['outputDir']
                                            )
            if "nii" in str_file:
                med2image_args['outputDir'] = os.path.join(med2image_args['outputDir'], str_file)
                os.mkdir(med2image_args['outputDir'])
            med2image_ns    = Namespace(**med2image_args)
            imgConverter    = med2image.object_factoryCreate(med2image_ns).C_convert

            # At time of dev, the `imgConverter.run()` does not return anything.
            if imgConverter: imgConverter.run()

        return {
            'status':           b_status,
            'str_path':         str_path,
            'l_fileProbed':     l_fileProbed,
            'd_convert':        d_convert
        }

    # def filelist_prune(self, at_data, *args, **kwargs) -> dict:
    #     """
    #     Given a list of files, possibly prune list by
    #     interal self.args['filter'].
    #     """

    #     b_status    : bool      = True
    #     l_file      : list      = []
    #     str_path    : str       = at_data[0]
    #     al_file     : list      = at_data[1]

    #     if len(self.args['filter']):
    #         al_file = [x for x in al_file if self.args['filter'] in x]

    #     if len(al_file):
    #         al_file.sort()
    #         l_file      = al_file
    #         b_status    = True
    #     else:
    #         self.dp.qprint( "No valid files to analyze found in path %s!" %
    #                         str_path, comms = 'warn', level = 5)
    #         l_file      = None
    #         b_status    = False
    #     return {
    #         'status':   b_status,
    #         'l_file':   l_file
    #     }

    def med2image(self) -> dict:
        """
        The main entry point for connecting methods of this class
        to the appropriate callbacks of the `pftree.tree_process()`.
        Note that the return json of each callback is available to
        the next callback in the queue as the second tuple value in
        the first argument passed to the callback.
        """
        d_med2image     : dict    = {}

        other.mkdir(self.args['outputDir'])
        d_med2image     = self.pf_tree.tree_process(
                            inputReadCallback       = self.inputReadCallback,
                            analysisCallback        = self.inputAnalyzeCallback,
                            outputWriteCallback     = None,
                            persistAnalysisResults  = False
        )
        return d_med2image

    def run(self, *args, **kwargs) -> dict:
        """
        This base run method should be called by any descendent classes
        since this contains the calls to the first `pftree` prove as well
        as any (overloaded) file filtering.
        """
        b_status        : bool  = False
        b_timerStart    : bool  = False
        d_pfdo          : dict  = {}
        d_med2image     : dict  = {}

        # pudb.set_trace()
        self.dp.qprint(
                "Starting pfdo_med2image run... (please be patient while running)",
                level = 1
        )

        for k, v in kwargs.items():
            if k == 'timerStart':   b_timerStart    = bool(v)

        if b_timerStart:    other.tic()

        d_pfdo          = super().run(
                            JSONprint   = False,
                            timerStart  = False
        )

        if d_pfdo['status']:
            d_med2image     = self.med2image()

        d_ret = {
            'status':           b_status,
            'd_pfdo':           d_pfdo,
            'd_med2image':      d_med2image,
            'runTime':          other.toc()
        }

        if self.args['json']:
            self.ret_dump(d_ret, **kwargs)
        else:
            self.dp.qprint('Returning from pfdo_med2image class run...', level = 1)

        return d_ret