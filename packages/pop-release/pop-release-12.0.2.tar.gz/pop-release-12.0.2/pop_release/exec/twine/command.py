from typing import List

import io
import twine.commands.check as tw_check
import twine.commands.register as tw_register
import twine.commands.upload as tw_upload

__virtualname__ = "cmd"


async def check(hub, dists: List[str], strict: bool = False):
    """
    Verify the named distribution files
    :param hub:
    :param dists:
    :param strict:
    """
    if isinstance(dists, str):
        dists = dists.split()
    with io.StringIO() as output:
        try:
            failure = tw_check.check(dists=dists, strict=strict, output_stream=output)

            ret = output.getvalue()

            return {"result": not failure, "ret": ret, "comment": None}
        except Exception as e:
            return {"result": False, "ret": str(e), "comment": e.__class__}


async def register(hub, ctx, package: str):
    """
    Register a package name with PyPi

    :param hub:
    :param ctx:
    :param package:
    """
    try:
        tw_register.register(register_settings=ctx.acct.settings, package=package)
        return {"result": True, "ret": "Success!", "comment": None}
    except Exception as e:
        return {"result": False, "ret": str(e), "comment": e.__class__}


async def upload(hub, ctx, dists: List[str]):
    try:
        if isinstance(dists, str):
            dists = dists.split()
            tw_upload.upload(upload_settings=ctx.acct.settings, dists=dists)
            return {"result": True, "ret": "Success", "comment": None}
    except Exception as e:
        return {"result": False, "ret": str(e), "comment": e.__class__}
