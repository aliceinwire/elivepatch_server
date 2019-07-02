#!/usr/bin/env python
# -*- coding: utf-8 -*-

# (c) 2017, Alice Ferrazzi <alice.ferrazzi@gmail.com>
# Distributed under the terms of the GNU General Public License v2 or later

import subprocess
import os
import fileinput
import tempfile
import shutil


class PaTch(object):

    def __init__(self, base_dir, base_config_path):
        self.base_dir = base_dir
        self.base_config_path = base_config_path

        self.__kernel_source_dir__ = os.path.join(self.base_dir, 'usr/src/linux/')

    def build_livepatch(self, vmlinux, jobs, debug=True):
        """
        Function for building the livepatch

        :param vmlinux: path to the vmlinux file
        :param debug: copy build.log in the base directory
        :return: void
        """
        vmlinux_source = os.path.join(self.__kernel_source_dir__, vmlinux)
        kpatch_cachedir = os.path.join(self.base_dir, 'kpatch')

        os.makedirs(kpatch_cachedir)
        if not os.path.isfile(vmlinux_source):
            self.build_kernel(jobs)

        bashCommand = ['kpatch-build',
                       '-s', self.__kernel_source_dir__,
                       '-v', vmlinux_source,
                       '-j', str(jobs),
                       '-c', 'config',
                       '-n', 'elivepatch-main',
                       '--skip-gcc-check',
                       'main.patch']
        if debug:
            bashCommand.extend(['--skip-cleanup'])
            bashCommand.extend(['-dddd'])
        _command(bashCommand, self.base_dir, {'CACHEDIR': kpatch_cachedir})
        if debug:
            shutil.copy(os.path.join(kpatch_cachedir, 'build.log'), self.base_dir)

    def get_kernel_sources(self, kernel_version, debug=True):
        """
        Function for download the kernel sources

        :return: void
        """
        try:
            _command(['git', 'clone', 'https://github.com/aliceinwire/gentoo-sources_overlay.git'])
        except:
            print('git clone failed.')

        ebuild_path = os.path.join('gentoo-sources_overlay', 'sys-kernel', 'gentoo-sources', 'gentoo-sources-' +
                                   kernel_version + '.ebuild')
        print(ebuild_path)
        if os.path.isfile(ebuild_path):
            # Use a private tmpdir for portage
            with tempfile.TemporaryDirectory(dir=self.base_dir) as portage_tmpdir:
                print('base_dir: ' + str(self.base_dir) + ' PORTAGE_TMPDIR: ' + str(portage_tmpdir))
                # portage_tmpdir is not always working with root privileges
                if debug:
                    if os.geteuid() != 0:
                        env = {'ROOT': self.base_dir, 'PORTAGE_CONFIGROOT': self.base_dir, 'PORTAGE_TMPDIR': portage_tmpdir,
                               'PORTAGE_DEBUG': '1'}
                    else:
                        env = {'ROOT': self.base_dir, 'PORTAGE_CONFIGROOT': self.base_dir, 'PORTAGE_TMPDIR': self.base_dir,
                               'PORTAGE_DEBUG': '1'}
                else:
                    if os.geteuid() != 0:
                        env = {'ROOT': self.base_dir, 'PORTAGE_CONFIGROOT': self.base_dir, 'PORTAGE_TMPDIR': portage_tmpdir}
                    else:
                        env = {'ROOT': self.base_dir, 'PORTAGE_CONFIGROOT': self.base_dir, 'PORTAGE_TMPDIR': self.base_dir}
                _command(['ebuild', ebuild_path, 'digest', 'clean', 'merge'], env=env)
                kernel_sources_status = True
        else:
            print('ebuild not present')
            kernel_sources_status = None
        return kernel_sources_status

    def build_kernel(self, jobs):
        kernel_config_path = os.path.join(self.__kernel_source_dir__, '.config')

        if 'CONFIG_DEBUG_INFO=y' in open(self.base_config_path).read():
            print("DEBUG_INFO correctly present")
        elif 'CONFIG_DEBUG_INFO=n' in open(self.base_config_path).read():
            print("changing DEBUG_INFO to yes")
            for line in fileinput.input(self.base_config_path, inplace=1):
                print(line.replace("CONFIG_DEBUG_INFO=n", "CONFIG_DEBUG_INFO=y"))
        else:
            print("Adding DEBUG_INFO for getting kernel debug symbols")
            for line in fileinput.input(self.base_config_path, inplace=1):
                print(line.replace("# CONFIG_DEBUG_INFO is not set", "CONFIG_DEBUG_INFO=y"))
        shutil.copyfile(self.base_config_path, kernel_config_path)
        # olddefconfig default everything that is new from the configuration file
        _command(['make', 'olddefconfig'], self.__kernel_source_dir__)
        # copy the olddefconfig generated config file back,
        # so that we don't trigger a config restart when kpatch-build runs
        shutil.copyfile(kernel_config_path, self.base_config_path)
        _command(['make', '-j', str(jobs)], self.__kernel_source_dir__)
        _command(['make', 'modules'], self.__kernel_source_dir__)


def _command(bashCommand, kernel_source_dir=None, env=None):
        """
        Popen override function

        :param bashCommand: List of command arguments to execute
        :param kernel_source_dir: String with the directory where the command is executed
        :param env: Dictionary for setting system environment variable
        :return: void
        """
        # Inherit the parent environment and update the private copy
        if env:
            process_env = os.environ.copy()
            process_env.update(env)
            env = process_env

        if kernel_source_dir:
            print(bashCommand)
            process = subprocess.Popen(bashCommand, stdout=subprocess.PIPE,  cwd=kernel_source_dir, env=env)
            output, error = process.communicate()
            for output_line in output.split(b'\n'):
                print(output_line.strip().decode("utf-8"))
        else:
            print(bashCommand)
            process = subprocess.Popen(bashCommand, stdout=subprocess.PIPE, env=env)
            output, error = process.communicate()
            for output_line in output.split(b'\n'):
                print(output_line.strip().decode("utf-8"))
