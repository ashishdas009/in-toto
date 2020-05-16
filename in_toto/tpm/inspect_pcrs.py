"""
<Program Name>
  inspect_byproducts.py

<Author>
  Ashish Das <ashish.das@nyu.edu>

<Started>
  May 8, 2020

<Copyright>
  See LICENSE for licensing information.

<Requires>
  in-toto, tpm2-tss, tpm2-tools

<Purpose>
  Inspections constitute an important part of in-toto. The script take the path
  of a link file, a random string and an operator, which is used to compare
  a certain property of the link file with the random string.

  Suppose the link file is located at /user/abc/def/package.45fe325.link
  and the user wants to check whether for the corresponding step (hence the
  link file), the corresponding stderr field contains the string "test".

  The usage would be as follows:
  python inspect_byproducts.py -l  /user/abc/def/package.45fe325.link  -t
    environment -o contains test

  General usage:
  python inspect_byproducts.py -l  <path/to/link/metadata/file>  -t
    type -o [ is | is not | contains | contains not] <string to
    be tested>
"""

import os
import sys
import argparse
import json
import in_toto.log
from in_toto.models.link import Link as link_import
import securesystemslib.exceptions


def inspect_environment(link, type_link, operator, input_string):
    """
    <Purpose>
    A function which performs the inspection as described above depending on
    various arguments.

    <Arguments>
      link:
        the path to the link file

      _type:
        the type of link metadata

      std:
        whether to check stdout or stderr field

      operator:
        is | is not | contains | contains not

      input_string:
        the string to be checked

    <Exceptions>
      Raises KeyError, in case the field corresponding to the key
      in the dictionary is empty

    <Returns>
      Boolean
    """
    #import pudb; pudb.set_trace()
    with open(link) as fp:
        data = json.load(fp)
    imported_link = link_import.read(data["signed"])
    envir = imported_link.__getattribute__(type_link) 

    if operator == 'is':
      if envir == input_string:
        return True

    elif operator == 'is-not':
      if envir != input_string:
        return True

    elif operator == 'contains':
        if "pcr" in envir.keys():
            return True

    elif operator == 'contains-not':
      if envir.find(input_string) == -1:
        return True
    else:
        raise Exception(
            "Invalid operator {}. Valid operators: is | is-not | contains | "
            "contains-not".format(operator))

    return False


def parse_args():
    """
    <Purpose>
      A function which parses the user supplied arguments.

    <Arguments>
      None

    <Exceptions>
      None

    <Returns>
      Parsed arguments (args object)
    """
    parser = argparse.ArgumentParser(
        description="Inspects the byproducts of a step")

    in_toto_args = parser.add_argument_group("in-toto-inspection options")

    in_toto_args.add_argument("-l", "--link", type=str, required=True,
                              help="Path to the link file to be inspected",
                              metavar="<Path to link metadata>")

    in_toto_args.add_argument("-t", "--type", choices=['environment'],
                             type=str, required=True, help="Type of "
                            "link metadata to inspect")

    in_toto_args.add_argument("-o", "--operator", choices=['is', 'is-not',
                              'contains', 'contains-not'], type=str,
                              required=True, help="whether "
                              "the type of link metadata is, is not,"
                              "contains, contains not, the input string")

    in_toto_args.add_argument("string", type=str,
                              help="The string to compare with the specified "
                              "link metadata type in the specified link file",
                              metavar="<String to compare>")

    args = parser.parse_args()
    args.operator = args.operator.lower()
    #args.type = args.type.lower()

    return args

def main():
    """
    First calls parse_args() to parse the arguments and then calls
    inspect_byproducts to inspect the byproducts
    """
    #import pudb; pudb.set_trace()
    args = parse_args()
    print(args)

    try:
        if inspect_environment(args.link, args.type, args.operator, args.string):
            return 0
        else:
            sys.exit(1)
    except Exception as e:
      print('The following error occured', e)
      sys.exit(2)


if __name__ == "__main__":
    main()
