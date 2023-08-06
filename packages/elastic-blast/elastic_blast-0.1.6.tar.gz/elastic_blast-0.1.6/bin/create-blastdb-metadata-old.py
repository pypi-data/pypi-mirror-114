#!/usr/bin/env python3
#                           PUBLIC DOMAIN NOTICE
#              National Center for Biotechnology Information
#  
# This software is a "United States Government Work" under the
# terms of the United States Copyright Act.  It was written as part of
# the authors' official duties as United States Government employees and
# thus cannot be copyrighted.  This software is freely available
# to the public for use.  The National Library of Medicine and the U.S.
# Government have not placed any restriction on its use or reproduction.
#   
# Although all reasonable efforts have been taken to ensure the accuracy
# and reliability of the software and data, the NLM and the U.S.
# Government do not and cannot warrant the performance or results that
# may be obtained by using this software or data.  The NLM and the U.S.
# Government disclaim all warranties, express or implied, including
# warranties of performance, merchantability or fitness for any particular
# purpose.
#   
# Please cite NCBI in any work or product based on this material.
"""
create-blastdb-metadata.py - See DESC constant below

Author: Greg Boratyn (boratyng@ncbi.nlm.nih.gov)
Created: Wed 26 May 2020 10:09:23 PM EDT
"""
import os
import argparse
import json
import logging
from pathlib import Path
from elb import VERSION
from elb.util import UserReportError
from elb.util import config_logging, safe_exec

DESC = r"""An application that creates metadata files for BLAST databases"""


def main():
    """ Entry point into this program. """
    METADATA_VERSION = '1.1'

    try:
        parser = create_arg_parser()
        args = parser.parse_args()
        config_logging(args)

        dbname = os.path.basename(args.db)
        metadata = {'version': METADATA_VERSION,
                    'dbname': dbname}

        cmd = 'blastdbcmd -list . -remove_redundant_dbs -list_outfmt'.split() +  ['%f\t%p\t%t\t%l\t%n\t%d\t%U']
        os.chdir('x')
        p = safe_exec(cmd)
#        print(p.stdout.decode())
        
        for line in p.stdout.decode().split('\n'):
            fields = line.rstrip().split('\t')
            if os.path.basename(fields[0]) != dbname:
                continue

            metadata['dbtype'] = fields[1]
            metadata['description'] = fields[2]
            metadata['number-of-letters'] = fields[3]
            metadata['number-of-sequences'] = fields[4]
            metadata['last-updated'] = fields[5]
            metadata['bytes-total'] = fields[6]
            break
        

        if 'description' not in metadata:
            raise UserReportError(returncode=255,
                                  message='Database was not found')

        cmd = f'blastdbcmd -db {dbname} -info'
        p = safe_exec(cmd)
        num_volumes = 0
        
        lines = p.stdout.decode().split('\n')

        for num, line in enumerate(lines):
            if line.startswith('Volumes:'):
                num_volumes = len(lines) - num - 2
                break

        metadata['number-of-volumes'] = num_volumes

        location = '/some/dir'
        files = [f'{location}/{str(i)}' for i in Path('.').glob(dbname + '*')]
        print(files)

        print(json.dumps(metadata, indent=4))

    except UserReportError as err:
        logging.error(err.message)
        return err.returncode

    return 0


def create_arg_parser():
    """ Create the command line options parser object for this script. """
    DFLT_LOGFILE = 'stderr'
    parser = argparse.ArgumentParser(prog=os.path.basename(os.path.splitext(sys.argv[0])[0]), 
                                     description=DESC)
    parser.add_argument("--db", type=str, help="BLAST database to search")
#    parser.add_argument("--db-source", type=str, help="Where NCBI-provided databases are downloaded from", choices=['AWS', 'GCP', 'NCBI'], default='AWS')
    parser.add_argument('--version', action='version',
                        version='%(prog)s ' + VERSION)
    parser.add_argument("--logfile", default=DFLT_LOGFILE, type=str,
                        help="Default: " + DFLT_LOGFILE)
    parser.add_argument("--loglevel", default='INFO',
                        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
    return parser


if __name__ == "__main__":
    import sys, traceback
    try:
        sys.exit(main())
    except Exception as e:
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)

