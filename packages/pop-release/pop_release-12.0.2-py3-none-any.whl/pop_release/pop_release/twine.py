# Import python libs
import pathlib


async def push(hub, ctx, root_path: pathlib.Path):
    """
    Push the build up to pypi!
    """
    ret = await hub.exec.twine.cmd.check(str(root_path / "dist" / "*"))
    if not ret.result:
        raise RuntimeError("Dist files failed check")

    ret = await hub.exec.twine.cmd.upload(ctx, str(root_path / "dist" / "*"))
    if not ret.result:
        raise RuntimeError(f"{ret.comment}: Dist files failed to upload")
