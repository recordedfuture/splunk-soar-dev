import tarfile
import os
import re
from invoke import task
from invoke.collection import Collection

RELEASE = "4.4.3"
BUILD_DIR = "pkg_build"
PACKAGE = f"recordedfuture-{RELEASE}.tgz"

PACKAGES = [
    "recorded_future_reputation_test.tgz",
    "recorded_future_intelligence_test.tgz",
    "recorded_future_reputation_parameter_test.tgz",
    "recorded_future_intelligence_parameter_test.tgz",
    "recorded_future_alert_test.tgz",
    "recorded_future_threat_assessment_test.tgz",
]
DIST_DIR = "playbook_build"
PRIVATE_KEYWORDS = re.compile(r"recfut|@recordedfuture")
PLAYBOOK_PATH = "./integration_tests/playbooks"


@task
def clean(c):
    """
    Removes build directory and earlier packaged release
    """
    c.run(f"rm -rf {BUILD_DIR}")
    c.run(f"rm -rf {PACKAGE}")


@task
def check_black(c):
    """Check that code complies with black requirements"""
    c.run("ruff format --check . --line-length 145")


@task
def black(c):
    """Run black on the code"""
    c.run("ruff format . --line-length 145")


@task(check_black)
@task(clean)
def build(c):
    """Collect everything to pkg_build directory"""
    c.run(
        f"""
        rsync -ra splunk-soar/* {BUILD_DIR} \
            --exclude=*.pyc \
            --exclude=.github \
            --exclude=tasks.py \
            --exclude=.git \
            --exclude=*.tgz \
            --exclude=venv \
            --exclude=pkg_build \
    """
    )


@task(build)
def package(c):
    """Package the app for uploading to splunk-soar"""
    c.run(f"tar cvfz {PACKAGE} pkg_build")


@task
def clean_playbook(c):
    """Clean out the playbook packages"""
    c.run(f"rm -rf {DIST_DIR}")


@task(pre=[clean_playbook])
def playbook_package(c):
    """Make playbook packages"""
    for pkg in PACKAGES:
        target = os.path.join(DIST_DIR, pkg)
        _create_package(c, target)


def _create_package(c, target):
    """Private method ensuring playbook packages are created"""

    def read_files(package_name):
        for ext in [".json", ".py"]:
            with open(f"{PLAYBOOK_PATH}/{package_name}/{package_name}{ext}", "r") as file:
                yield from file

    if not os.path.exists(DIST_DIR):
        os.makedirs(DIST_DIR)
    package_name = os.path.basename(target).replace(".tgz", "")

    # Check for private keywords
    if any(PRIVATE_KEYWORDS.search(line) for line in read_files(package_name)):
        print(f"The playbook {package_name} contains internal emails or hosts.")
        for line in read_files(package_name):
            if PRIVATE_KEYWORDS.search(line):
                print(line)
        exit(1)

    # Create tar.gz package
    with tarfile.open(target, "w:gz") as tar:
        for file in [
            f"{PLAYBOOK_PATH}/{package_name}/{package_name}.json",
            f"{PLAYBOOK_PATH}/{package_name}/{package_name}.py",
        ]:
            tar.add(file, arcname=os.path.basename(file))


# currently not used
# playbook = Collection("playbook")
# playbook.add_task(playbook_package, name="package")
# namespace.add_collection(playbook)


namespace = Collection()
namespace.add_task(black)
namespace.add_task(check_black)
namespace.add_task(package)
namespace.add_task(build)
namespace.add_task(clean)
