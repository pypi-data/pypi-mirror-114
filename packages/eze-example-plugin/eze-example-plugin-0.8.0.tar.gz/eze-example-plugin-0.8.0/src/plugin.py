"""Lists out the inbuilt plugins in Example"""
from src.example_reporter import ExampleReporter
from src.example_tool import ExampleTool


def get_reporters() -> dict:
    """Return the reporters in plugin"""
    return {
        "example-reporter": ExampleReporter,
    }


def get_tools() -> dict:
    """Return the tools in plugin"""
    return {
        "example-tool": ExampleTool,
    }
