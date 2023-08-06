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

import json
import pathlib
from collections import defaultdict

import yaml

from jsonpointer import resolve_pointer
from jsonschema import Draft7Validator, draft7_format_checker
from jsonref import JsonRef
from cliff.command import Command


class TestSchemas(Command):
    """Validate examples against schemas"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument("filename")
        parser.add_argument("-d", "--detail", action="store_true")
        parser.add_argument(
            "-p",
            "--path",
            default="/components/schemas",
            help="Path to where the schemas are located",
        )
        parser.add_argument(
            "-s",
            "--strict",
            action="store_true",
            help="Default to 'allowExtraProperties: false'",
        )
        return parser

    def take_action(self, args):
        fn = pathlib.Path(args.filename)
        with fn.open() as fp:
            if fn.suffix.lower() == ".json":
                spec = json.load(fp)
            elif fn.suffix.lower() == ".yaml":
                spec = yaml.safe_load(fp)
            else:
                raise ValueError(f"Unsupported filetype {fn.suffix}")

        spec = JsonRef.replace_refs(spec)
        errors = defaultdict(list)
        schemas = resolve_pointer(spec, args.path)
        for schema_name, schema in schemas.items():
            example = schema.get("example")
            if not example:
                continue
            schema.setdefault("additionalProperties", False)
            try:
                validator = Draft7Validator(
                    schema, format_checker=draft7_format_checker
                )
                for error in validator.iter_errors(example):
                    errors[schema_name].append(error)
            except Exception as error:
                errors[schema_name].append(error)
        print(f"Validated {len(schemas)} schemas:")
        print(f"  - {len(errors)} had errors")

        if errors and args.detail:
            print()
            print("Detailed error list follows:")
            for sname, errs in sorted(errors.items()):
                print(f"#/components/schemas/{sname} ({len(errs)} errors):")
                for err in errs:
                    path = "/".join(str(p) for p in err.path)
                    if not path:
                        path = (
                            "["
                            + "/".join(str(p) for p in err.schema_path)
                            + "]"
                        )
                    print(f"    - {path}: {err.message}")
