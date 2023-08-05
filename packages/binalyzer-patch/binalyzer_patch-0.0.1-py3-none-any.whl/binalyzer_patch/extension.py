"""
    binalyzer_patch.extension
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    This module implements the Binalyzer patch extension.
"""
import os

from binalyzer_core import (
    Binalyzer,
    BinalyzerExtension,
)

class PatchExtension(BinalyzerExtension):
    def __init__(self, binalyzer=None):
        super(PatchExtension, self).__init__(binalyzer, "patch")

    def init_extension(self):
        super(PatchExtension, self).init_extension()

    def apply(self, input_file, patch_file, output_file):
        self.binalyzer.xml.from_str(
            patch_file.read(), 
            input_file.read()
        )

        for patch_template in self.binalyzer.template.patches.children:
            patch_template.value = patch_template.text

        output_file.write(self.binalyzer.template.value)
