"""
    binalyzer_patch.cli
    ~~~~~~~~~~~~~~~~~~~

    Patch extension for the *binalyzer* command.
"""
import io
import logging
import click

from binalyzer import (
    Binalyzer,
    ExpandedFile,
    XMLTemplateParser,
)

from binalyzer_patch import PatchExtension

logger = logging.getLogger('binalyzer.patch')

stdout_formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

stdout_handler = logging.StreamHandler()
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.setFormatter(stdout_formatter)

logger.addHandler(stdout_handler)
logger.setLevel(logging.DEBUG)


@click.command()
@click.option('--input-file', '-i', required=True, type=ExpandedFile("rb"), help='The binary file to patch.')
@click.option('--patch-file', '-p', required=True, type=ExpandedFile("r"), help='The patch file.')
@click.option('--output-file', '-o', required=True, type=ExpandedFile("wb"), help='The patched binary file.')
def patch(input_file, patch_file, output_file):
    """Patch a binary file using a patch file.
    """
    logger.info(f"Patching file {input_file.name}")
    
    binalyzer = Binalyzer()
    PatchExtension(binalyzer)
    binalyzer.patch.apply(input_file, patch_file, output_file)
    
    logger.info(f"The file has been successfully patched.")
