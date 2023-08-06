import inspect
import re
from pathlib import Path

from tecton import conf
from tecton._internals import metadata_service
from tecton_proto.args.repo_metadata_pb2 import SourceInfo
from tecton_proto.data.workspace_pb2 import Workspace
from tecton_proto.metadataservice.metadata_service_pb2 import GetWorkspaceRequest

# Matches frame strings such as "<string>"
SKIP_FRAME_REGEX = re.compile("\<.*\>")


def get_current_workspace():
    return conf.get("TECTON_WORKSPACE")


def get_fco_source_info() -> SourceInfo:
    from tecton.cli.cli import _repo_root

    source_info = SourceInfo()
    if not _repo_root:
        pass
    else:
        frames = inspect.stack()
        repo_root_path = Path(_repo_root)
        for frame in frames:
            if SKIP_FRAME_REGEX.match(frame.frame.f_code.co_filename) is not None:
                continue
            frame_path = Path(frame.frame.f_code.co_filename).resolve()
            if frame_path.exists() and (repo_root_path in frame_path.parents):
                rel_filename = frame_path.relative_to(repo_root_path)
                source_info.source_lineno = str(frame.lineno)
                source_info.source_filename = str(rel_filename)
                break
    return source_info


def get_workspace(workspace_name: str) -> Workspace:
    request = GetWorkspaceRequest()
    request.workspace_name = workspace_name
    response = metadata_service.instance().GetWorkspace(request)
    return response.workspace


def is_materializable_workspace(workspace_name: str) -> bool:
    return get_workspace(workspace_name).capabilities.materializable
