# Copyright (C) 2011-2021 Andrea Francia Bereguardo(PV) Italy
import argparse

from .fstab import volume_of
from .list import TrashDirsSelector
from .trash import (TopTrashDirRules, TrashDirReader, path_of_backup_copy,
                    print_version, println, Clock, parse_deletion_date,
                    trash_dir_found, UserInfoProvider, AllUsersInfoProvider)
from .trash import TrashDirsScanner
from .trash import EX_OK
import os
import sys
from trashcli.list_mount_points import os_mount_points
from datetime import datetime
from trashcli.fs import FileSystemReader
from trashcli.fs import FileRemover
from trashcli import trash


def main(argv=sys.argv,
         stdout=sys.stdout,
         stderr=sys.stderr,
         environ=os.environ):
    return EmptyCmd(
        out=stdout,
        err=stderr,
        environ=environ,
        list_volumes=os_mount_points,
        now=datetime.now,
        file_reader=FileSystemReader(),
        getuid=os.getuid,
        file_remover=FileRemover(),
        version=trash.version,
        volume_of=volume_of
    ).run(*argv)


class Errors:
    def __init__(self, program_name, err):
        self.program_name = program_name
        self.err = err

    def print_error(self, msg):
        self.err.write("%s: %s\n" % (self.program_name, msg))


def description(program_name, printer):
    printer.usage('Usage: %s [days]' % program_name)
    printer.summary('Purge trashed files.')
    printer.options(
       "  --version   show program's version number and exit",
       "  -h, --help  show this help message and exit")
    printer.bug_reporting()


class MainLoop:
    def __init__(self, trash_dir, trashcan):
        self.trash_dir = trash_dir
        self.trashcan = trashcan

    def do_loop(self, trash_dirs, delete_mode):
        for event, args in trash_dirs:
            if event == trash_dir_found:
                trash_dir_path, volume = args
                for trashinfo_path in self.trash_dir.list_trashinfo(trash_dir_path):
                    if delete_mode.ok_to_delete(trashinfo_path):
                        self.trashcan.delete_trashinfo_and_backup_copy(trashinfo_path)
                for orphan in self.trash_dir.list_orphans(trash_dir_path):
                    self.trashcan.delete_orphan(orphan)

class EmptyCmd:
    def __init__(self,
                 out,
                 err,
                 environ,
                 list_volumes,
                 now,
                 file_reader,
                 getuid,
                 file_remover,
                 version,
                 volume_of):

        self.out = out
        self.err = err
        self.file_reader = file_reader
        self.version = version
        self.clock = Clock(now, environ)
        file_remover_with_error = FileRemoveWithErrorHandling(file_remover,
                                                              self.print_cannot_remove_error)
        trashcan = CleanableTrashcan(file_remover_with_error)
        user_info_provider = UserInfoProvider(environ, getuid)
        user_dir_scanner = TrashDirsScanner(user_info_provider,
                                            list_volumes,
                                            TopTrashDirRules(file_reader))
        all_users_info_provider = AllUsersInfoProvider()
        all_users_scanner = TrashDirsScanner(all_users_info_provider,
                                             list_volumes,
                                             TopTrashDirRules(file_reader))
        self.selector = TrashDirsSelector(user_dir_scanner.scan_trash_dirs(),
                                          all_users_scanner.scan_trash_dirs(),
                                          volume_of)
        trash_dir = TrashDirReader(self.file_reader)
        self.main_loop = MainLoop(trash_dir, trashcan)

    def run(self, *argv):
        program_name = os.path.basename(argv[0])
        self.errors = Errors(program_name, self.err)

        parser = make_parser()
        parsed = parser.parse_args(argv[1:])

        if parsed.version:
            print_version(self.out, program_name, self.version)
        elif parsed.print_time:
            now_value = self.clock.get_now_value(self.errors)
            println(self.out, now_value.replace(microsecond=0).isoformat())
        else:
            if not parsed.days:
                delete_mode = DeleteAnything()
            else:
                delete_mode = DeleteAccordingDate(self.file_reader.contents_of,
                                                  self.clock,
                                                  int(parsed.days),
                                                  self.errors)
            trash_dirs = self.selector.select(parsed.all_users,
                                              parsed.user_specified_trash_dirs)
            self.main_loop.do_loop(trash_dirs, delete_mode)
        return EX_OK


    def print_cannot_remove_error(self, path):
        self.errors.print_error("cannot remove %s" % path)


class FileRemoveWithErrorHandling:
    def __init__(self, file_remover, on_error):
        self.file_remover = file_remover
        self.on_error = on_error

    def remove_file(self, path):
        try:
            return self.file_remover.remove_file(path)
        except OSError:
            self.on_error(path)

    def remove_file_if_exists(self, path):
        try:
            return self.file_remover.remove_file_if_exists(path)
        except OSError:
            self.on_error(path)


class DeleteAccordingDate:
    def __init__(self, contents_of, clock, max_age_in_days, errors):
        self.contents_of = contents_of
        self.clock = clock
        self.max_age_in_days = max_age_in_days
        self.errors = errors

    def ok_to_delete(self, trashinfo_path):
        contents = self.contents_of(trashinfo_path)
        now_value = self.clock.get_now_value(self.errors)
        deletion_date = parse_deletion_date(contents)
        if deletion_date is not None:
            if older_than(self.max_age_in_days, now_value, deletion_date):
                return True
        return False


class DeleteAnything:

    def ok_to_delete(self, _trashinfo_path):
        return True


def older_than(days_ago, now_value, deletion_date):
    from datetime import timedelta
    limit_date = now_value - timedelta(days=days_ago)
    return deletion_date < limit_date


class CleanableTrashcan:
    def __init__(self, file_remover):
        self._file_remover = file_remover

    def delete_orphan(self, path_to_backup_copy):
        self._file_remover.remove_file(path_to_backup_copy)

    def delete_trashinfo_and_backup_copy(self, trashinfo_path):
        backup_copy = path_of_backup_copy(trashinfo_path)
        self._file_remover.remove_file_if_exists(backup_copy)
        self._file_remover.remove_file(trashinfo_path)


def make_parser():
    parser = argparse.ArgumentParser(
        description='Purge trashed files.',
        epilog='Report bugs to https://github.com/andreafrancia/trash-cli/issues')
    parser.add_argument('--version', action='store_true', default=False,
                        help="show program's version number and exit")
    parser.add_argument('--trash-dir', action='append', default=[],
                        metavar='TRASH_DIR',
                        dest='user_specified_trash_dirs',
                        help='specify the trash directory to use')
    parser.add_argument('--print-time', action='store_true', dest='print_time',
                        help=argparse.SUPPRESS)
    parser.add_argument('--all-users', action='store_true', dest='all_users',
                        help=argparse.SUPPRESS)
    parser.add_argument('days', action='store', default=None, type=int,
                        nargs='?')
    return parser


class Guard:
    def __init__(self, emptier):
        self.emptier = emptier

    def ask_the_user(self, user, trash_dirs):
        trash_dirs_list = list(trash_dirs)
        if user.do_you_wanna_empty_trash_dirs(trash_dirs_list):
            self.emptier(trash_dirs_list)
