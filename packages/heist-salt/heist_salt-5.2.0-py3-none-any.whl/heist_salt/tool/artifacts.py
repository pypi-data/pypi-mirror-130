import pathlib


def get_artifact_dir(hub):
    """
    function to get the full path to artifacts directory
    with the pkg_type included
    """
    pkg_type = "singlebin"
    if hub.OPT.heist.onedir:
        pkg_type = "onedir"
    artifacts_dir = pathlib.Path(hub.OPT.heist.artifacts_dir, pkg_type)
    if not artifacts_dir.is_dir():
        artifacts_dir.mkdir()
    return str(artifacts_dir)
