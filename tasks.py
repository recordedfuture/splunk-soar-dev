from invoke import task

RELEASE = "4.4.3"
BUILD_DIR = "pkg_build"
PACKAGE = f"recordedfuture-{RELEASE}.tgz"


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
    c.run("black --check . --line-length 145")


@task
def black(c):
    """Run black on the code"""
    c.run("black . --line-length 145")


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
