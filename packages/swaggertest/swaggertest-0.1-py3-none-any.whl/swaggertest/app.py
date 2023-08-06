# Copyright 2021 Arborian Consulting, LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pdb
import sys
import traceback

from cliff.app import App
from cliff.commandmanager import CommandManager


class SwaggerTest(App):
    app = None

    @classmethod
    def main(cls, argv=sys.argv[1:]):
        app = cls()
        cls.app = app
        return app.run(argv)

    @classmethod
    def debug_hook(cls, value, type, tb):
        traceback.print_exception(type, value, tb)
        print()
        pdb.pm()

    def __init__(self):
        super().__init__(
            description="Swagger testing tool",
            version="0.1",
            command_manager=CommandManager("swaggertest.app"),
            deferred_help=True,
        )

    def initialize_app(self, argv):
        super().initialize_app(argv)
        if self.options.pdb:
            sys.excepthook = self.debug_hook

    def build_option_parser(self, description, version, argparse_kwargs=None):
        parser = super().build_option_parser(
            description, version, argparse_kwargs
        )
        parser.add_argument("--pdb", action="store_true")
        return parser
