#!/usr/bin/env python3.5

import  sys
import  os
import  json
import  pudb
sys.path.insert(1, os.path.join(os.path.dirname(__file__), '..'))

from    pfmisc._colors import Colors
from    pfmisc.debug   import debug
from    pfmisc.C_snode import *
from    pfmisc.error   import *

class someOtherClass():
    """
    Some other class
    """

    def __init__(self, *args, **kwargs):
        """
        """

        self.dp             = debug(
                                verbosity   = 0,
                                level       = -1,
                                within      = "someOtherClass"
                            )
        self.log            = self.dp.qprint

    def say(self, msg):
        print('\n* Now we are in a different class in this module...')
        print('* Note the different class and method in the debug output.')
        print('* calling: self.dp.qprint(msg):')
        self.log(msg, level = -1)

class pfmisc():
    """
    Example of how to use the local misc dependencies
    """

    # An error declaration block
    _dictErr = {
        'someError1'   : {
            'action'        : 'trying to parse image file specified, ',
            'error'         : 'wrong format found. Must be [<index>:]<filename>',
            'exitCode'      : 1},
        'someError2': {
            'action'        : 'trying to read input <tagFileList>, ',
            'error'         : 'could not access/read file -- does it exist? Do you have permission?',
            'exitCode'      : 20
            }
        }

    def col2_print(self, str_left, str_right):
        print(Colors.WHITE +
              ('%*s' % (self.LC, str_left)), end='')
        print(Colors.LIGHT_BLUE +
              ('%*s' % (self.RC, str_right)) + Colors.NO_COLOUR)

    def __init__(self, *args, **kwargs):
        """

        Holder for constructor of class -- allows for explicit setting
        of member 'self' variables.

        :return:
        """
        self.LC             = 40
        self.RC             = 40
        self.args           = None
        self.str_desc       = 'pfmisc'
        self.str_name       = self.str_desc
        self.str_version    = ''

        self.dp             = debug(verbosity   = 1,
                                    within      = 'pfmisc',
                                    hostnamecol = 7,
                                    methodcol   = 10)
        self.log            = self.dp.qprint

        self.dp2            = debug(verbosity   = 1,
                                    within      = 'pfmisc',
                                    debugToFile = True,
                                    debugFile   = '/tmp/pfmisc.txt')
        self.log2           = self.dp2.qprint

    def demo(self, *args, **kwargs):
        """
        Simple run method
        """
        # pudb.set_trace()
        print('\n* calling: self.dp.qprint("Why hello there, world!"):')
        self.log("Why hello there, world!")

        print('\n* calling: self.dp.qprint("Why hello there, world!", colorize = False):')
        self.log("Why hello there, world!", colorize = False)

        print('\n* calling: self.dp.qprint("Why hello there, world!", colorize = False, syslog = False):')
        self.log("Why hello there, world!", colorize = False, syslog = False)

        print('\n* calling: self.dp2.qprint("Why hello there, world! In a debugging file!"):')
        self.log2("Why hello there, world! In a debugging file!")
        print('\n* Check on /tmp/pfmisc.txt')

        print('\n* calling: self.dp.qprint("Why hello there, world! With teeFile!", teeFile="/tmp/pfmisc-teefile.txt", teeMode = "w+"):')
        self.log("Why hello there, world! With teeFile!", teeFile="/tmp/pfmisc-teefile.txt", teeMode = "w+")
        print('\n* Check on /tmp/pfmisc-teefile.txt')

        other = someOtherClass()
        other.say("And this is from a different class")

        for str_comms in ['status', 'error', 'tx', 'rx']:
            print('\n* calling: self.dp.qprint("This string is tagged with %s" % str_comms, ', end='')
            print("comms = '%s')" % str_comms)
            self.log("This string is tagged with '%s'" % str_comms, comms = str_comms)

        print("And here is warning...")
        warn(
            self, 'someError1',
            header  = 'This is only a warning!',
            drawBox = True
        )
