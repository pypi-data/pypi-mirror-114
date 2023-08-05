"""
Main module for eze example reporter

Exposed via entry_point
One example reporter where the results of an analysis tool can be returned in a specific output (format/via)
"""
from eze.core.reporter import ReporterMeta
from eze.core.tool import ScanResult

from src import __version__


class ExampleReporter(ReporterMeta):
    """Example report class for echoing all output into the console"""

    REPORTER_NAME: str = "example-reporter"
    SHORT_DESCRIPTION: str = "example copy: standard example reporter"
    INSTALL_HELP: str = """example copy: Installation guide for ExampleTool

Aka: just run pip install one-two-three
"""
    MORE_INFO: str = """example copy: more help can be found on
https://example.example.com"""
    LICENSE: str = """MIT"""
    EZE_CONFIG: dict = {}

    @staticmethod
    def check_installed() -> str:
        """Method for detecting if reporter installed and ready to run report, returns version installed"""
        return __version__

    async def run_report(self, scan_results: list):
        """Method for taking scans and turning them into report output
        Types of scans: Scans vulnerabilities, sboms, and warnings"""
        print(f"Running '{self.REPORTER_NAME}' reporter")
        for scan_result_raw in scan_results:
            scan_result: ScanResult = scan_result_raw
            print(f"Example scan result '{scan_result.tool}' report output")
