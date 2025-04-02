from pathlib import Path
import json
import ast
import os

ROOT = Path(__file__).parent.parent


def extract_test_names(test_folder_path):
    """
    Extract all test function and method names from Python test files in the given folder.

    Args:
        test_folder_path (str): Path to the folder containing test files.

    Returns:
        dict: Dictionary with file names as keys and lists of test names as values.
    """
    test_files = {}

    # Walk through the test directory
    for root, _, files in os.walk(test_folder_path):
        for file in files:
            # Check if file matches test_*.py pattern
            if file.startswith("test_") and file.endswith(".py"):
                file_path = os.path.join(root, file)
                test_names = []

                try:
                    # Parse Python file
                    with open(file_path, "r") as f:
                        tree = ast.parse(f.read(), filename=file)

                    # Extract function and method names
                    for node in ast.walk(tree):
                        # Check for standalone test functions
                        if isinstance(node, ast.FunctionDef) and node.name.startswith(
                            "test_"
                        ):
                            test_names.append(node.name)

                        # Check for test methods in classes
                        elif isinstance(node, ast.ClassDef):
                            # If class name suggests it's a test class
                            if "Test" in node.name:
                                for item in node.body:
                                    if isinstance(
                                        item, ast.FunctionDef
                                    ) and item.name.startswith("test_"):
                                        test_names.append(f"{item.name}")

                    if test_names:
                        test_files[file] = test_names
                except Exception as e:
                    print(f"Error processing file {file}: {e}")

    return test_files


def test_all_actions_tested():
    """
    All actions need to have a test method named the same as their identifier.
    An action with the name "ip reputation" has the identifier "ip_reputation"
    """

    config = ROOT / "splunk-soar" / "recordedfuture.json"
    with config.open() as f:
        data = json.load(f)
    actions = data["actions"]
    action_ids = set([a["identifier"].replace("-", "_") for a in actions])

    test_methods = extract_test_names(ROOT / "integration_tests")
    test_set = set()
    for test_file, methods in test_methods.items():
        msg = f"Test method names are not globally unique from file {test_file}: {methods}"
        assert test_set.isdisjoint(set(methods)), msg
        test_set = test_set | set(methods)

    test_names = set([name[5:] for name in test_set])

    msg = f"These actions have no tests: {action_ids - test_names}"
    assert action_ids.issubset(test_names), msg
