import sys
import subprocess
import os


def main():
    command = sys.argv[1]

    # Define test directories and corresponding coverage targets
    test_config = {
        "unit": {"dir": "tests/unit_tests", "cov": ["config", "src"]},
        "integration": {"dir": "tests/integration_tests", "cov": []},
        "component": {"dir": "tests/component_tests", "cov": []},
        "e2e": {"dir": "tests/e2e_tests", "cov": []},
        "all": {"dir": "tests", "cov": ["config", "src"]},
    }

    # Check to see if a command was supplied for the test run
    if command == "all":
        # Run coverage on unit tests only, then run all other tests
        env = os.environ.copy()
        env["ENV"] = "test"

        # Run linting first
        subprocess.run(["flake8", "."])
        subprocess.run(["sqlfluff", "lint", "src", "config", "scripts"])

        # Run unit tests with coverage
        unit_cov_command = (
            "coverage run --source=config,src "
            "--omit=*/__init__.py -m pytest --verbose tests/unit_tests "
            "&& coverage report -m && coverage html "
            "&& coverage report --fail-under=90"
        )
        subprocess.run(unit_cov_command, shell=True, env=env)

        # Run other tests without coverage
        for test_type in ["integration", "component", "e2e"]:
            test_dir = test_config[test_type]["dir"]
            subprocess.run(
                f"pytest --verbose {test_dir}", shell=True, env=env
            )

    elif command in test_config:
        # Access the test_config dictionary to get the test directory
        # and coverage targets
        test_dir = test_config[command]["dir"]
        cov_sources = ",".join(test_config[command]["cov"])

        # Build the test command for tests with coverage
        if cov_sources:
            cov_command = (
                f"coverage run --source={cov_sources} "
                f"--omit=*/__init__.py -m pytest --verbose {test_dir} "
                "&& coverage report -m && coverage html "
                "&& coverage report --fail-under=90"
            )
        else:
            cov_command = f"pytest --verbose {test_dir}"

        # Set up environment for subprocess
        env = os.environ.copy()
        env["ENV"] = "test"
        subprocess.run(cov_command, shell=True, env=env)
    elif command == "lint":
        subprocess.run(["flake8", "."])
        subprocess.run(["sqlfluff", "lint", "src", "config", "scripts"])
    else:
        raise ValueError(f"Unknown command: {command}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise ValueError(
            "Usage: run_tests.py <unit|integration|component|e2e|all|lint>"
        )
    else:
        main()
