#!/usr/bin/env python
import os
import sys
from pathlib import Path
from argparse import ArgumentParser, Namespace, ArgumentDefaultsHelpFormatter
from chris_plugin import chris_plugin, PathMapper
from concurrent.futures import ThreadPoolExecutor
from typing import Optional, Literal, Sequence, BinaryIO
from civet.extraction.hemisphere import Side, HemisphereMask
import subprocess as sp
from loguru import logger

SIDE_OPTIONS = ('left', 'right', 'auto', 'none')
SideStr = Literal['left', 'right', 'auto', 'none']

parser = ArgumentParser(description='ChRIS plugin wrapper for sphere_mesh',
                        formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument('-s', '--side', default='auto', choices=SIDE_OPTIONS,
                    help='brain hemisphere side. "auto" => infer from file name')
parser.add_argument('-p', '--pattern', default='**/*.mnc',
                    help='pattern for file names to include')
parser.add_argument('-q', '--quiet', action='store_true',
                    help='disable status messages')


def pick_side(mask: Path, side: SideStr) -> Optional[Side]:
    if side == 'left':
        return Side.LEFT
    if side == 'right':
        return Side.RIGHT
    if side == 'auto':
        path = str(mask).lower()
        if 'left' in path:
            return Side.LEFT
        if 'right' in path:
            return Side.RIGHT
        raise ValueError(f'Substring "left" nor "right" found in: {path}')
    if side == 'none':
        return None
    raise ValueError(f'side must be one of: {SIDE_OPTIONS}')


def curry_log(log: BinaryIO):
    def run_with_log(cmd: Sequence[str | os.PathLike]) -> None:
        log.write(b'[sphere_mesh_wrapper]$> ')
        log.write(str(cmd).encode('utf-8'))
        log.write(b'\n')
        log.flush()
        sp.run(cmd, stderr=log, stdout=log, check=True)
    return run_with_log


def sphere_mesh_wrapper(mask: Path, surface: Path, side: SideStr):
    log_path = surface.with_suffix('.sphere_mesh.log')
    try:
        logger.info('Processing {} to {}, log: {}', mask, surface, log_path)
        with log_path.open('wb') as log:
            HemisphereMask(mask)\
                .just_sphere_mesh(pick_side(mask, side))\
                .save(surface, shell=curry_log(log))
        logger.info('Completed {}', surface)
    except Exception as e:
        logger.exception('Failed to process {}', mask)
        raise e


@chris_plugin(
    title='sphere_mesh ChRIS plugin wrapper',
    category='Surface Extraction',
    parser=parser
)
def main(options: Namespace, inputdir: Path, outputdir: Path):
    if options.quiet:
        logger.remove()
        logger.add(sys.stderr, level='WARNING')

    results = []
    with ThreadPoolExecutor(max_workers=len(os.sched_getaffinity(0))) as pool:
        mapper = PathMapper.file_mapper(inputdir, outputdir, glob=options.pattern, suffix='.obj')
        for mnc, obj in mapper:
            results.append(pool.submit(sphere_mesh_wrapper, mnc, obj, options.side))

    for future in results:
        future.exception()


if __name__ == '__main__':
    main()
