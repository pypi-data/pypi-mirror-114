"""
Main module for eze example tool

Exposed via entry_point
One example tool where the results of an analysis tool can be generated
"""
from eze.core.enums import VulnerabilitySeverityEnum, ToolType, SourceType
from eze.core.tool import (
    ToolMeta,
    ScanResult,
    Vulnerability,
)
from eze.utils.io import create_tempfile_path

from src import __version__


class ExampleTool(ToolMeta):
    """Example Tool Class"""

    TOOL_NAME: str = "example-tool"
    TOOL_TYPE: ToolType = ToolType.MISC
    SOURCE_SUPPORT: list = [SourceType.ALL]
    SHORT_DESCRIPTION: str = "example copy: opensource static key scanner"
    INSTALL_HELP: str = """example copy: Installation guide for ExampleTool

Aka: just run pip install one-two-three
"""
    MORE_INFO: str = """example copy: more help can be found on
https://example.example.com"""
    LICENSE: str = """MIT"""
    # THESE PARAMETERS WILL BE AUTOMATICALLY EXTRACTED FROM .ezerc
    # tool key
    #
    # POPULATED KEYS WILL BE self.config
    EZE_CONFIG: dict = {
        "REPORT_FILE": {
            "type": str,
            "default": create_tempfile_path("tmp-example-tool-report.json"),
            "default_help_value": "<tempdir>/.eze-temp/tmp-example-tool-report.json",
            "help_text": "output report location (will default to tmp file otherwise)",
        },
        #
        "CONFIG_FILE": {"type": str, "default": None},
        "SOURCE": {"type": str, "default": "."},
    }

    DEFAULT_SEVERITY = "medium"
    TOOL_CLI_CONFIG = {
        "CMD_CONFIG": {
            # Basic command required to run the tool. Arguments like --no-git, --quiet can also be added here.
            "BASE_COMMAND": "exampletool",
            # Additional arguments passed by the client using a config file.
            "ARGUMENTS": ["ARG1", "ARG2"],
            # Possible arguments to be passed via .ezerc file.
            "FLAGS": {
                "SOURCE": "--path ",
                "REPORT_FILE": "--report ",
                "CONFIG_FILE": "-c ",
            },
        }
    }

    @staticmethod
    def check_installed() -> str:
        """Checks if the tools is installed and ready to run scan, returns version installed"""
        return __version__

    async def run_scan(self) -> ScanResult:
        """Method for running a synchronous scan using tool, returns a parsed json response"""
        # Configuration keys available in self.config
        #
        # aka for our example config's REPORT_FILE
        # from eze.utils.io import load_json
        # parsed_json = load_json(self.config["REPORT_FILE"])
        #
        # Configuration self.config can also be combined to call cli commands using
        # from eze.utils.cli import run_cli_command
        # completed_process = run_cli_command(self.TOOL_CLI_CONFIG["CMD_CONFIG"], self.config, self.TOOL_NAME)
        #
        # Generate and Return the ScanResult
        example_vulnerability: Vulnerability = Vulnerability(
            {
                "name": "Some High Vulnerability",
                "severity": VulnerabilitySeverityEnum.high.name,
            }
        )
        report: ScanResult = ScanResult(
            {
                # array of eze.core.tool.Vulnerability
                "vulnerabilities": [example_vulnerability],
                # dict version of Cyclonedx JSON format SBOM
                "bom": None,
                # String Array of warnings
                "warnings": [],
            }
        )

        return report
