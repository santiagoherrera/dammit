#!/usr/bin/env python
import os

from doit.action import CmdAction
from doit.tools import LongRunning
from doit.task import clean_targets

from .utils import clean_folder
from ..profile import profile_task
from ..utils import which, doit_task


@doit_task
@profile_task
def get_transdecoder_orf_task(input_filename, params=None):
    '''Get a task to run `Transdecoder.LongOrfs`.

    Args:
        input_filename (str): FASTA file to analyze.
        params (list): Extra parameters to pass to the executable.

    Returns:
        dict: A doit task.
    '''

    name = 'TransDecoder.LongOrfs:' + os.path.basename(input_filename)

    exc = which('TransDecoder.LongOrfs')
    cmd = [exc, '-t', input_filename]
    if params is not None:
        cmd.extend(params)
    cmd = ' '.join(cmd)

    return {'name': name,
            'actions': [cmd],
            'file_dep': [input_filename],
            'targets': [input_filename + '.transdecoder_dir/longest_orfs.pep'],
            'clean': [(clean_folder, [input_filename + '.transdecoder_dir'])]}


@doit_task
@profile_task
def get_transdecoder_predict_task(input_filename, pfam_filename=None, params=None):
    '''Get a task to run `TransDecoder.Predict`.

    Args:
        input_filename (str): The FASTA file to analyze.
        pfam_filename (str): If HMMER has been run against Pfam, pass this
            file name to `--retain_pfam_hits`.
        params (list): Extra parameters to pass to the executable.

    Returns:
        dict: A doit task.
    '''

    name = 'TransDecoder.Predict:' + os.path.basename(input_filename)

    exc = which('TransDecoder.Predict')
    cmd = [exc, '-t', input_filename]
    file_dep = [input_filename,
                input_filename + '.transdecoder_dir/longest_orfs.pep']
    if pfam_filename is not None:
        cmd.extend(['--retain_pfam_hits', pfam_filename])
        file_dep.append(pfam_filename)
    if params is not None:
        cmd.extend(params)
    cmd = ' '.join(cmd)

    return {'name': name,
            'actions': [cmd],
            'file_dep': file_dep,
            'targets': [input_filename + '.transdecoder' + ext \
                        for ext in ['.bed', '.cds', '.pep', '.gff3', '.mRNA']],
            'clean': [clean_targets,
                     (clean_folder, [input_filename + '.transdecoder_dir'])]}
