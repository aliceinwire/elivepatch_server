#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# (c) 2017, Alice Ferrazzi <alice.ferrazzi@gmail.com>
# Distributed under the terms of the GNU General Public License v2 or later


import os
import re
import werkzeug
import shutil
from flask import jsonify, make_response
from flask_restful import Resource, reqparse, fields, marshal
from .livepatch import PaTch

pack_fields = {
    'KernelVersion': fields.String,
    'UUID': fields.String

}

packs = {
    'id': 1,
    'KernelVersion': None,
    'UUID': None
}


def check_uuid(uuid):
    """
    Check uuid is in the correct format
    :param uuid:
    :return:
    """
    if not uuid:
        print('uuid is missing')
    else:
        # check uuid format
        prog = re.compile('^\w{8}-\w{4}-\w{4}-\w{4}-\w{12}$')
        result = prog.match(uuid)
        if result:
            print('UUID: ' + str(uuid))
            return uuid
        print('uuid format is not correct')


def get_tmp_uuid_dir(uuid):
    return os.path.join('/tmp/', 'elivepatch-' + uuid)

def get_cache_uuid_dir(uuid, filename):
    livepatch_folder = os.path.join('/tmp/', 'livepatch-' + uuid)
    livepatch_file = os.path.join(livepatch_folder, filename)
    return livepatch_folder, livepatch_file

class SendLivePatch(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('KernelVersion', type=str, required=False,
                                   help='No task title provided',
                                   location='json')
        self.reqparse.add_argument('UUID', type=str, required=False,
                                   help='No task title provided',
                                   location='json')
        super(SendLivePatch, self).__init__()
        pass

    def get(self):
        args = self.reqparse.parse_args()
        print("get livepatch: " + str(args))
        # check if is a valid UUID request
        args['UUID'] = check_uuid(args['UUID'])
        livepatch_saving_folder, livepatch_saving_file = get_cache_uuid_dir(args['UUID'], 'livepatch.ko')
        try:
            with open(livepatch_saving_file, 'rb') as fp:
                response = make_response(fp.read())
                response.headers['content-type'] = 'application/octet-stream'
                return response
        except:
            return make_response(jsonify({'message': 'These are not the \
            patches you are looking for'}), 403)

    def post(self):
        return make_response(jsonify({'message': 'These are not the \
        patches you are looking for'}), 403)


class GetFiles(Resource):

    def __init__(self, **kwargs):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('KernelVersion', type=str, required=False,
                                   help='No task title provided',
                                   location='headers')
        self.reqparse.add_argument('UUID', type=str, required=False,
                                   help='No task title provided',
                                   location='headers')
        self.cmdline_args = kwargs['cmdline_args']
        super(GetFiles, self).__init__()
        pass

    def get(self):
        return make_response(jsonify({'message': 'These are not the \
        patches you are looking for'}), 403)

    def post(self):
        args = self.reqparse.parse_args()
        args['UUID'] = check_uuid(args['UUID'])
        parse = reqparse.RequestParser()
        parse.add_argument('patch', action='append', type=werkzeug.datastructures.FileStorage,
                           location='files')
        parse.add_argument('main_patch', action='append', type=werkzeug.datastructures.FileStorage,
                           location='files')
        parse.add_argument('config', type=werkzeug.datastructures.FileStorage,
                           location='files')
        file_args = parse.parse_args()

        uuid_dir = get_tmp_uuid_dir(args['UUID'])
        if os.path.exists(uuid_dir):
            print('the folder: "' + uuid_dir + '" is already present')
            return {'the request with ' + args['UUID'] + ' is already present'}, 201
        else:
            print('creating: "' + uuid_dir + '"')
            os.makedirs(uuid_dir)

        print("file get config: " + str(file_args))
        configFile = file_args['config']
        # saving config file
        configFile_name = os.path.join(uuid_dir, file_args['config'].filename)
        configFile.save(configFile_name)

        lpatch = PaTch(uuid_dir, configFile_name)

        # saving incremental patches
        incremental_patches_directory = os.path.join(uuid_dir, 'etc', 'portage', 'patches',
                                                     'sys-kernel', 'gentoo-sources')
        if os.path.exists(incremental_patches_directory):
            print('the folder: "' + uuid_dir + '" is already present')
            return {'the request with ' + args['UUID'] + ' is already present'}, 201
        else:
            print('creating: '+incremental_patches_directory)
            os.makedirs(incremental_patches_directory)
        try:
            for patch in file_args['patch']:
                print(str(patch))
                patchfile = patch
                patchfile_name = patch.filename
                patch_fulldir_name = os.path.join(incremental_patches_directory, patchfile_name)
                patchfile.save(patch_fulldir_name)
        except:
            print('no incremental patches')

        # saving main patch
        print(str(file_args['main_patch']))
        main_patchfile = file_args['main_patch'][0]
        main_patchfile_name = main_patchfile.filename
        main_patch_fulldir_name = os.path.join(uuid_dir, main_patchfile_name)
        main_patchfile.save(main_patch_fulldir_name)

        # check vmlinux presence if not rebuild the kernel
        kernel_sources_status = lpatch.get_kernel_sources(args['KernelVersion'])
        if not kernel_sources_status:
            return make_response(jsonify({'message': 'gentoo-sources not available'}), 403)
        lpatch.build_livepatch('vmlinux', jobs=self.cmdline_args.jobs)
        livepatch_full_path = os.path.join(uuid_dir, 'kpatch-main.ko')
        livepatch_saving_folder, livepatch_saving_file = get_cache_uuid_dir(args['UUID'], 'livepatch.ko')
        if os.path.exists(livepatch_saving_folder):
            print('saving livepatch to: '+ str(livepatch_saving_file))
            try:
                shutil.move(livepatch_full_path, livepatch_saving_file)
            except:
                print('live patch not generated')
                print('check build.log at:' + str(livepatch_saving_folder + '/build.log'))
                try:
                    shutil.move(uuid_dir + '/kpatch/build.log', livepatch_saving_folder + '/build.log')
                except:
                    print('no build.log generated')
        else:
            print('creating: "' + str(livepatch_saving_folder) + '"')
            os.makedirs(livepatch_saving_folder)
            print('saving livepatch to: '+ str(livepatch_saving_file))
            try:
                shutil.move(livepatch_full_path, livepatch_saving_file)
            except:
                print('live patch not generated')
                print('check build.log at:' + str(livepatch_saving_folder + '/build.log'))
                try:
                    shutil.move(uuid_dir + '/kpatch/build.log', livepatch_saving_folder + '/build.log')
                except:
                    print('no build.log generated')

        pack = {
           'id': packs['id'] + 1,
            'KernelVersion': None,
            'UUID' : args['UUID']
        }
        return {'get_config': marshal(pack, pack_fields)}, 201

    def __del__(self):
        args = self.reqparse.parse_args()
        print('deleting folder: '+ get_tmp_uuid_dir(args['UUID']))
        shutil.rmtree(get_tmp_uuid_dir(args['UUID']))
