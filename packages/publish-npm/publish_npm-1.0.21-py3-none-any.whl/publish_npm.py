#!/usr/bin/env python

import argparse
import hashlib
import json
import os
import pkg_resources
import re
import subprocess
import sys

if sys.version_info < (3, 0):
    printf("Error: This script requires Python 3.")
    sys.exit(1)

# Constants
VERSION = pkg_resources.get_distribution("publish_npm").version
DIR = os.getcwd()
PROJECT_NAME = os.path.basename(DIR)
PACKAGE_JSON = "package.json"
PACKAGE_JSON_PATH = os.path.join(DIR, PACKAGE_JSON)


def main():
    args = parse_command_line_arguments()

    # Check to see if the "package.json" file exists
    if not os.path.isfile(PACKAGE_JSON_PATH):
        error(
            'Failed to find the "{}" file in the current working directory.'.format(
                PACKAGE_JSON
            )
        )

    # Check to see if we are logged in to npm
    completed_process = subprocess.run(
        ["npm", "whoami"],
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    if completed_process.returncode != 0:
        error(
            'The "npm whoami" command failed, so you are probably not logged in. Try doing "npm login".'
        )

    # Update the dependencies to the latest versions
    if not args.skip_update:
        # Get the hash before we potentially modify the "package.json" file
        before_hash = get_hash_of_package_json()

        printf("Updating NPM dependencies...")
        completed_process = subprocess.run(
            [
                "npx",
                "npm-check-updates",
                "--upgrade",
                "--packageFile",
                PACKAGE_JSON,
                "--loglevel",
                "silent",
            ],
            shell=True,
        )
        if completed_process.returncode != 0:
            error(
                'Failed to update the "{}" dependencies to the latest versions.'.format(
                    PACKAGE_JSON
                )
            )

        after_hash = get_hash_of_package_json()
        if before_hash != after_hash:
            # The package.json file was modified, so install the new dependencies
            printf("Installing NPM dependencies...")
            completed_process = subprocess.run(
                ["npm", "install", "--silent"], shell=True
            )
            if completed_process.returncode != 0:
                error('Failed to run "npm install".')

    # Before we increment the version number, make sure that the program compiles
    if is_typescript_project():
        printf("Testing to see if the project compiles...")
        compile_typescript()

    # Increment the version number
    version = get_version_from_package_json()
    if not args.skip_increment:
        version = increment_version(version)
        put_version(version)

    # Build the program again so that the new version number is included in the compiled code
    if is_typescript_project():
        printf("Re-compiling the project...")
        compile_typescript()

    git_commit_if_changes(version)

    # Publish
    printf("Publishing to NPM...")
    completed_process = subprocess.run(
        [
            "npm",
            "publish",
            "--access",
            "public",
        ],
        shell=True,
    )
    if completed_process.returncode != 0:
        error("Failed to npm publish.")

    # Done
    printf("Published {} version {} successfully.".format(PROJECT_NAME, version))


def parse_command_line_arguments():
    parser = argparse.ArgumentParser(
        description="Publish a new version of this package to NPM."
    )

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        help="display the version",
        version=VERSION,
    )

    parser.add_argument(
        "-s",
        "--skip-increment",
        action="store_true",
        help='do not increment the version number in the "{}" file'.format(
            PACKAGE_JSON
        ),
    )

    parser.add_argument(
        "-u",
        "--skip-update",
        action="store_true",
        help='do not update NPM dependencies in the "{}" file'.format(PACKAGE_JSON),
    )

    return parser.parse_args()


def get_hash_of_package_json():
    with open(PACKAGE_JSON_PATH, "rb") as f:
        file_hash = hashlib.md5()
        file_contents = f.read()
        file_hash.update(file_contents)

        return file_hash.hexdigest()


def get_version_from_package_json():
    with open(PACKAGE_JSON_PATH, "r") as file_handle:
        package_json = json.load(file_handle)

    if "version" not in package_json:
        error('Failed to find the version in the "{}" file.'.format(PACKAGE_JSON_PATH))

    return package_json["version"]


def increment_version(version: str):
    match = re.search(r"(.+\..+\.)(.+)", version)
    if not match:
        error('Failed to parse the version number of "{}".'.format(version))
    version_prefix = match.group(1)
    patch_version = int(match.group(2))  # i.e. the third number
    incremented_patch_version = patch_version + 1
    incremented_version = version_prefix + str(incremented_patch_version)

    return incremented_version


def put_version(version: str):
    with open(PACKAGE_JSON_PATH, "r") as file_handle:
        package_json = json.load(file_handle)

    package_json["version"] = version

    with open(PACKAGE_JSON_PATH, "w", newline="\n") as file_handle:
        json.dump(package_json, file_handle, indent=2, separators=(",", ": "))
        file_handle.write("\n")

    completed_process = subprocess.run(["npx", "sort-package-json"], shell=True)
    if completed_process.returncode != 0:
        error('Failed to sort the "{}" file.'.format(PACKAGE_JSON))


def is_typescript_project():
    with open(PACKAGE_JSON_PATH, "r") as file_handle:
        package_json = json.load(file_handle)

    return (
        "dependencies" in package_json and "typescript" in package_json["dependencies"]
    ) or (
        "devDependencies" in package_json
        and "typescript" in package_json["devDependencies"]
    )


def compile_typescript():
    build_script_path = os.path.join(DIR, "build.sh")
    if os.path.isfile(build_script_path):
        completed_process = subprocess.run(["bash", build_script_path], shell=True)
        if completed_process.returncode != 0:
            error('Failed to run the "build.sh" script.')
    else:
        completed_process = subprocess.run(["rm", "-rf", "dist"], shell=True)
        if completed_process.returncode != 0:
            error('Failed to remove the "dist" directory.')

        completed_process = subprocess.run(["npx", "tsc"], shell=True)
        if completed_process.returncode != 0:
            error('Failed to build the project with "npx tsc".')


def git_commit_if_changes(version):
    # Check to see if this is a git repository
    completed_process = subprocess.run(
        ["git", "status"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    if completed_process.returncode != 0:
        error("This is not a git repository.")

    # Check to see if there are any changes
    # https://stackoverflow.com/questions/3878624/how-do-i-programmatically-determine-if-there-are-uncommitted-changes
    completed_process = subprocess.run(["git", "diff-index", "--quiet", "HEAD", "--"])
    changes_to_existing_files = completed_process.returncode != 0

    # Check to see if there are any untracked files
    # https://stackoverflow.com/questions/11021287/git-detect-if-there-are-untracked-files-quickly
    completed_process = subprocess.run(
        ["git", "ls-files", "--other", "--directory", "--exclude-standard"],
        stdout=subprocess.PIPE,
    )
    if completed_process.returncode != 0:
        error("Failed to git ls-files.")
    git_output = completed_process.stdout.decode("utf-8")
    untracked_files_exist = git_output is not None and git_output.strip() != ""

    if not changes_to_existing_files and not untracked_files_exist:
        printf("There are no changes to push to git.")
        return

    # Commit to the repository
    printf("Committing to the Git repository...")
    completed_process = subprocess.run(["git", "add", "-A"])
    if completed_process.returncode != 0:
        error("Failed to git add.")
    completed_process = subprocess.run(["git", "commit", "-m", version])
    if completed_process.returncode != 0:
        error("Failed to git commit.")
    completed_process = subprocess.run(["git", "pull", "--rebase"])
    if completed_process.returncode != 0:
        error("Failed to git pull.")
    completed_process = subprocess.run(["git", "push"])
    if completed_process.returncode != 0:
        error("Failed to git push.")

    printf('Pushed a commit to git for version "{}".'.format(version))


def error(msg):
    printf("Error: {}".format(msg))
    sys.exit(1)


def printf(msg):
    print(msg, flush=True)


if __name__ == "__main__":
    main()
