import json
import unittest
from json import JSONDecodeError
from typing import AnyStr, List, Union, Pattern, Dict, Any

from dnastack.__main__ import dnastack as cli
from click.testing import CliRunner


class BaseCliTestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        self.runner = CliRunner()
        super().__init__(*args, **kwargs)

    def assertCommand(
        self,
        command: List[AnyStr],
        exit_code: int = 0,
        json_output: bool = False,
        output_pattern: Union[Pattern[AnyStr], AnyStr] = None,
    ) -> Union[Dict[AnyStr, Any], AnyStr, None]:
        result = self.runner.invoke(cli, ["--debug"] + command)

        self.assertEqual(
            result.exit_code,
            exit_code,
            f"[dnastack {' '.join([str(c) for c in command])}] "
            f"{'succeeded' if exit_code else 'failed'} "
            f"unexpectedly, expected exit code [{exit_code}],"
            f" got [{result.exit_code}], output: {result.output}",
        )

        if output_pattern:
            self.assertRegex(result.output, output_pattern)

        if json_output:
            try:
                out = json.loads(result.output)
            except JSONDecodeError as j:
                self.fail(
                    f"Unable to parse output as JSON for command [{' '.join(command)}] (output: {result.output})"
                )
        else:
            out = result.output

        return out
