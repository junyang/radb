import os
import sys
import configparser
import argparse
import atexit
import getpass

try:
    import readline
except ImportError:
    _readline_available = False
else:
    _readline_available = True

from radb.db import DB
from radb.parse import ParsingError,\
    statement_string_from_stdin, one_statement_from_string, RACompleter
from radb.typesys import ValTypeChecker, TypeSysError
from radb.views import ViewCollection
from radb import utils
from radb.ast import Context, ValidationError, ExecutionError, execute_from_file

import logging
logger = logging.getLogger('ra')

def main():

    # read system defaults:
    sys_configfile = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sys.ini')
    sys_config = configparser.ConfigParser()
    if sys_config.read(sys_configfile) == []:
        print('ERROR: required system configuration file {} not found'.format(sys_configfile))
        sys.exit(1)
    defaults = dict(sys_config.items(configparser.DEFAULTSECT))

    # parse input arguments:
    parser = argparse.ArgumentParser()
    parser.add_argument('--configfile', '-c', type=str, default=defaults['configfile'],
                        help='configuration file (default: {})'.format(defaults['configfile']))
    parser.add_argument('--password', '-p', action='store_true',
                        help='prompt for database password')
    parser.add_argument('--inputfile', '-i', type=str,
                        help='input file')
    parser.add_argument('--outputfile', '-o', type=str,
                        help='output file')
    parser.add_argument('--echo', '-e', action='store_true',
                        help='echo input')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='verbose output')
    parser.add_argument('--debug', '-d', action='store_true',
                        help='debug output')
    parser.add_argument('source', type=str, nargs='?', default=configparser.DEFAULTSECT,
                        help='data source, which can be the name of a configuration section'
                        ' (default: {}), or otherwise the name of the database to connect to'
                        ' (overriding the configuration default)'.format(configparser.DEFAULTSECT))
    args = parser.parse_args()

    # set up output replication + logging:
    if args.outputfile is not None:
        sys.stdout = utils.Tee(args.outputfile)
    logging.getLogger('ra').setLevel(logging.DEBUG if args.debug else\
                                     (logging.INFO if args.verbose else\
                                      logging.WARNING))
    logger_handler = logging.StreamHandler(sys.stdout)
    logger_handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
    logger.addHandler(logger_handler)

    # read user configuration file (starting with system defaults):
    config = configparser.ConfigParser(defaults)
    if config.read(os.path.expanduser(args.configfile)) == []:
        logger.warning('unable to read configuration file {}; resorting to system defaults'\
                       .format(os.path.expanduser(args.configfile)))

    # finalize configuration settings, using configuration file and command-line arguments:
    if args.source == configparser.DEFAULTSECT or config.has_section(args.source):
        configured = dict(config.items(args.source))
    else: # args.source is not a section in the config file; treat it as a database name:
        configured = dict(config.items(configparser.DEFAULTSECT))
        configured['db.database'] = args.source
    if args.password:
        configured['db.password'] = getpass.getpass('Database password: ')

    # connect to database:
    if 'db.database' not in configured:
        logger.warning('no database specified')
    try:
        db = DB(configured)
    except Exception as e:
        logger.error('failed to connect to database: {}'.format(e))
        sys.exit(1)

    # initialize type system:
    try:
        check = ValTypeChecker(configured['default_functions'], configured.get('functions', None))
    except TypeSysError as e:
        logger.error(e)
        sys.exit(1)

    # construct context (starting with empty view collection):
    context = Context(configured, db, check, ViewCollection())

    # finally, let's start:
    if args.inputfile is None: # interactive:
        if _readline_available:
            # set up command history file:
            historyfile = os.path.expanduser(configured['historyfile'])
            try:
                readline.read_history_file(historyfile)
                history_length = readline.get_history_length()
            except FileNotFoundError:
                open(historyfile, 'wb').close()
                history_length = 0
            def save_history(prev_history_length, historyfile):
                new_history_length = readline.get_current_history_length()
                readline.set_history_length(1000)
                readline.append_history_file(new_history_length - prev_history_length, historyfile)
            atexit.register(save_history, history_length, historyfile)
            # set up command completion:
            readline.set_completer_delims(readline.get_completer_delims().replace('\\', ''))
            readline.parse_and_bind('tab: complete')
            readline.set_completer(RACompleter().complete)
            atexit.register(lambda: readline.set_completer(None))
        print('{name}: {description}\nVersion {version} by {author} <{author_email}>\n{url}'.
              format(**{key: configured['setup.' + key]\
                        for key in ('name', 'description',
                                    'version', 'author', 'author_email',
                                    'url')}))
        for s in statement_string_from_stdin(echo=args.echo):
            logger.info('statement received:')
            for line in utils.number_lines(s):
                logger.info(line)
            try:
                ast = one_statement_from_string(s)
                logger.info('statement parsed:')
                logger.info(str(ast))
                ast.validate(context)
                logger.info('statement validated:')
                for line in ast.info():
                    logger.info(line)
                ast.execute(context)
            except (ParsingError, ValidationError, ExecutionError) as e:
                logger.error(e)
    else:
        try:
            execute_from_file(args.inputfile, context, echo=args.echo)
        except (IOError, ParsingError, ValidationError, ExecutionError) as e:
            logger.error(e)
            sys.exit(1)

if __name__ == '__main__':
    main()
