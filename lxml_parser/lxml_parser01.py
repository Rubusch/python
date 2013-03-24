#!/usr/bin/python

import sys
from os import path
from lxml import etree


def main(argv=sys.argv[1:]):
    if 0 == len(argv) or not path.isfile(argv[0]):
        print "usage: %s <path to .xml>" % sys.argv[0]
        sys.exit(1)
    xml=argv[0]


    ## Task
    #
    # list commands
    # //Command/ChildCommands/CommandSetting/Name
    #
    # followed by list of params
    # //Command/ChildCommands/CommandSetting/Parameters/ParameterSetting/Name
    #
    # with specific value(s) set
    # //Command/ChildCommands/CommandSetting/Parameters/ParameterSetting/Value


    ##
    filterlist = [
        "DefineVariable",
#        "Pause",

        "Discriminant",
        "ServiceId",
        "CommandId",
        "SequenceId",
        "SequenceInstanceId",
        "ModuleId",
        "ProcType",
        "TimeoutICM",
        "NrOfNormalEvents",
        "NormalEvent_WildCardEvent",
        "NrOfWarningEvents",
        "WarningEvent_WildCardEvent",
        "NrOfAnomalyEvents",
        "AnomalyEvent_WildCardEvent",
        "NrOfErrorEvents",
        "ErrorEvent_WildCardEvent",
        "NrOfDataEvents",
        "DataEvent_WildCardEvent"
        ]

    content = etree.parse( xml )
    elements = content.xpath( '//Command/ChildCommands/CommandSetting' )
    command_sequence = []
    for elem_command in elements:
        step = ""
        step = elem_command.xpath('./Name')[0].text
        if step in filterlist: continue ## RnD Tool params
        step += '( '
        separator = ''
        for elem_param in elem_command.xpath('Parameters/ParameterSetting'):
             param = separator
             tmp = elem_param.xpath('Name')[0].text
             if tmp in filterlist: continue ## RnD Tool params
             param += tmp
             param += ' = '
             separator=', '
             if 0 != len(elem_param.xpath('Value')):
                 param += '\"'
                 param += elem_param.xpath('Value')[0].text
                 param += '\"'
             else:
                 param = ''
             step += param
        step += ' )'
        command_sequence.append( step )
    for item in command_sequence:
        print( item )


## start
if __name__ == '__main__':
    main()

