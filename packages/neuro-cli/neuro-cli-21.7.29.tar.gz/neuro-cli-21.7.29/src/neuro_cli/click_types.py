import abc
import os
import re
from datetime import datetime, timedelta
from typing import (
    Generic,
    List,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    TypeVar,
    Union,
    cast,
)

import click
from click import BadParameter

from neuro_sdk import Client, LocalImage, Preset, RemoteImage, TagOption

from .parse_utils import (
    JobTableFormat,
    parse_ps_columns,
    parse_top_columns,
    to_megabytes,
)
from .root import Root

# NOTE: these job name defaults are taken from `platform_api` file `validators.py`
JOB_NAME_MIN_LENGTH = 3
JOB_NAME_MAX_LENGTH = 40
JOB_NAME_PATTERN = "^[a-z](?:-?[a-z0-9])*$"
JOB_NAME_REGEX = re.compile(JOB_NAME_PATTERN)
JOB_LIMIT_ENV = "NEURO_CLI_JOB_AUTOCOMPLETE_LIMIT"


# NOTE: these disk name valdation are taken from `platform_disk_api` file `schema.py`
DISK_NAME_MIN_LENGTH = 3
DISK_NAME_MAX_LENGTH = 40
DISK_NAME_PATTERN = "^[a-z](?:-?[a-z0-9])*$"
DISK_NAME_REGEX = re.compile(JOB_NAME_PATTERN)

_T = TypeVar("_T")


class AsyncType(click.ParamType, Generic[_T], abc.ABC):
    def convert(
        self, value: str, param: Optional[click.Parameter], ctx: Optional[click.Context]
    ) -> _T:
        assert ctx is not None
        root = cast(Root, ctx.obj)
        return root.run(self.async_convert(root, value, param, ctx))

    @abc.abstractmethod
    async def async_convert(
        self,
        root: Root,
        value: str,
        param: Optional[click.Parameter],
        ctx: Optional[click.Context],
    ) -> _T:
        pass

    def complete(
        self, ctx: click.Context, args: Sequence[str], incomplete: str
    ) -> List[Tuple[str, Optional[str]]]:
        root = cast(Root, ctx.obj)
        return root.run(self.async_complete(root, ctx, args, incomplete))

    @abc.abstractmethod
    async def async_complete(
        self, root: Root, ctx: click.Context, args: Sequence[str], incomplete: str
    ) -> List[Tuple[str, Optional[str]]]:
        pass


class LocalImageType(click.ParamType):
    name = "local_image"

    def convert(
        self, value: str, param: Optional[click.Parameter], ctx: Optional[click.Context]
    ) -> LocalImage:
        assert ctx is not None
        root = cast(Root, ctx.obj)
        client = root.run(root.init_client())
        return client.parse.local_image(value)


class RemoteTaglessImageType(click.ParamType):
    name = "image"

    def convert(
        self, value: str, param: Optional[click.Parameter], ctx: Optional[click.Context]
    ) -> RemoteImage:
        assert ctx is not None
        root = cast(Root, ctx.obj)
        client = root.run(root.init_client())
        return client.parse.remote_image(value, tag_option=TagOption.DENY)


class RemoteImageType(click.ParamType):
    name = "image"

    def __init__(self, tag_option: TagOption = TagOption.DEFAULT) -> None:
        self.tag_option = tag_option

    def convert(
        self, value: str, param: Optional[click.Parameter], ctx: Optional[click.Context]
    ) -> RemoteImage:
        assert ctx is not None
        root = cast(Root, ctx.obj)
        cluster_name = ctx.params.get("cluster")
        client = root.run(root.init_client())
        return client.parse.remote_image(
            value, tag_option=self.tag_option, cluster_name=cluster_name
        )


class LocalRemotePortParamType(click.ParamType):
    name = "local-remote-port-pair"

    def convert(
        self, value: str, param: Optional[click.Parameter], ctx: Optional[click.Context]
    ) -> Tuple[int, int]:
        try:
            local_str, remote_str = value.split(":")
            local, remote = int(local_str), int(remote_str)
            if not (0 < local <= 65535 and 0 < remote <= 65535):
                raise ValueError("Port should be in range 1 to 65535")
            return local, remote
        except ValueError as e:
            raise BadParameter(f"{value} is not a valid port combination: {e}")


LOCAL_REMOTE_PORT = LocalRemotePortParamType()


class MegabyteType(click.ParamType):
    name = "megabyte"

    def convert(
        self, value: str, param: Optional[click.Parameter], ctx: Optional[click.Context]
    ) -> int:
        if isinstance(value, int):
            return int(value / (1024 ** 2))
        return to_megabytes(value)


MEGABYTE = MegabyteType()


class JobNameType(click.ParamType):
    name = "job_name"

    def convert(
        self, value: str, param: Optional[click.Parameter], ctx: Optional[click.Context]
    ) -> str:
        if (
            len(value) < JOB_NAME_MIN_LENGTH
            or len(value) > JOB_NAME_MAX_LENGTH
            or JOB_NAME_REGEX.match(value) is None
        ):
            raise ValueError(
                f"Invalid job name '{value}'.\n"
                "The name can only contain lowercase letters, numbers and hyphens "
                "with the following rules: \n"
                "  - the first character must be a letter; \n"
                "  - each hyphen must be surrounded by non-hyphen characters; \n"
                f"  - total length must be between {JOB_NAME_MIN_LENGTH} and "
                f"{JOB_NAME_MAX_LENGTH} characters long."
            )
        return value


JOB_NAME = JobNameType()


class DiskNameType(click.ParamType):
    name = "disk_name"

    def convert(
        self, value: str, param: Optional[click.Parameter], ctx: Optional[click.Context]
    ) -> str:
        if (
            len(value) < DISK_NAME_MIN_LENGTH
            or len(value) > DISK_NAME_MAX_LENGTH
            or DISK_NAME_REGEX.match(value) is None
        ):
            raise ValueError(
                f"Invalid disk name '{value}'.\n"
                "The name can only contain lowercase letters, numbers and hyphens "
                "with the following rules: \n"
                "  - the first character must be a letter; \n"
                "  - each hyphen must be surrounded by non-hyphen characters; \n"
                f"  - total length must be between {DISK_NAME_MIN_LENGTH} and "
                f"{DISK_NAME_MAX_LENGTH} characters long."
            )
        return value


DISK_NAME = DiskNameType()


class JobColumnsType(click.ParamType):
    name = "columns"

    def convert(
        self,
        value: Union[str, JobTableFormat],
        param: Optional[click.Parameter],
        ctx: Optional[click.Context],
    ) -> JobTableFormat:
        if isinstance(value, list):
            return value
        return parse_ps_columns(value)


JOB_COLUMNS = JobColumnsType()


class TopColumnsType(click.ParamType):
    name = "columns"

    def convert(
        self,
        value: Union[str, JobTableFormat],
        param: Optional[click.Parameter],
        ctx: Optional[click.Context],
    ) -> JobTableFormat:
        if isinstance(value, list):
            return value
        return parse_top_columns(value)


TOP_COLUMNS = TopColumnsType()


class PresetType(AsyncType[str]):
    name = "preset"

    def _get_presets(
        self, ctx: Optional[click.Context], client: Client
    ) -> Mapping[str, Preset]:
        cluster_name = client.cluster_name
        if ctx:
            cluster_name = ctx.params.get("cluster", client.cluster_name)
        if cluster_name not in client.config.clusters:
            return {}
        return client.config.clusters[cluster_name].presets

    async def async_convert(
        self,
        root: Root,
        value: str,
        param: Optional[click.Parameter],
        ctx: Optional[click.Context],
    ) -> str:
        client = await root.init_client()
        if value not in self._get_presets(ctx, client):
            cluster_name = client.cluster_name
            if ctx:
                cluster_name = ctx.params.get("cluster", client.cluster_name)
            if cluster_name != client.cluster_name:
                error_message = (
                    f"Preset {value} is not valid for cluster {cluster_name}."
                )
            else:
                error_message = f"Preset {value} is not valid, "
                "run 'neuro config show' to get a list of available presets"
            raise click.BadParameter(
                error_message,
                ctx,
                param,
            )
        return value

    async def async_complete(
        self, root: Root, ctx: click.Context, args: Sequence[str], incomplete: str
    ) -> List[Tuple[str, Optional[str]]]:
        # async context manager is used to prevent a message about
        # unclosed session
        async with await root.init_client() as client:
            presets = list(self._get_presets(ctx, client))
            return [(p, None) for p in presets if p.startswith(incomplete)]


PRESET = PresetType()


class ClusterType(AsyncType[str]):
    name = "cluster"

    async def async_convert(
        self,
        root: Root,
        value: str,
        param: Optional[click.Parameter],
        ctx: Optional[click.Context],
    ) -> str:
        client = await root.init_client()
        if value not in client.config.clusters:
            raise click.BadParameter(
                f"Cluster {value} is not valid, "
                "run 'neuro config get-clusters' to get a list of available clusters",
                ctx,
                param,
            )
        return value

    async def async_complete(
        self, root: Root, ctx: click.Context, args: Sequence[str], incomplete: str
    ) -> List[Tuple[str, Optional[str]]]:
        # async context manager is used to prevent a message about
        # unclosed session
        async with await root.init_client() as client:
            clusters = list(client.config.clusters)
            return [(c, None) for c in clusters if c.startswith(incomplete)]


CLUSTER = ClusterType()


class JobType(AsyncType[str]):
    name = "job"

    async def async_convert(
        self,
        root: Root,
        value: str,
        param: Optional[click.Parameter],
        ctx: Optional[click.Context],
    ) -> str:
        return value

    async def async_complete(
        self, root: Root, ctx: click.Context, args: Sequence[str], incomplete: str
    ) -> List[Tuple[str, Optional[str]]]:
        async with await root.init_client() as client:
            ret: List[Tuple[str, Optional[str]]] = []
            now = datetime.now()
            limit = int(os.environ.get(JOB_LIMIT_ENV, 100))
            async with client.jobs.list(
                since=now - timedelta(days=7), reverse=True, limit=limit
            ) as it:
                async for job in it:
                    job_name = job.name or ""
                    for test in (
                        job.id,
                        job_name,
                        f"job:{job.id}",
                        f"job:/{job.owner}/{job.id}",
                        f"job://{job.cluster_name}/{job.owner}/{job.id}",
                    ):
                        if test.startswith(incomplete):
                            ret.append((test, job_name))

            return ret


JOB = JobType()


class DiskType(AsyncType[str]):
    name = "disk"

    async def async_convert(
        self,
        root: Root,
        value: str,
        param: Optional[click.Parameter],
        ctx: Optional[click.Context],
    ) -> str:
        return value

    async def async_complete(
        self, root: Root, ctx: click.Context, args: Sequence[str], incomplete: str
    ) -> List[Tuple[str, Optional[str]]]:
        async with await root.init_client() as client:
            ret: List[Tuple[str, Optional[str]]] = []
            async with client.disks.list(cluster_name=ctx.params.get("cluster")) as it:
                async for disk in it:
                    disk_name = disk.name or ""
                    for test in (
                        disk.id,
                        disk_name,
                    ):
                        if test.startswith(incomplete):
                            ret.append((test, disk_name))

            return ret


DISK = DiskType()


class ServiceAccountType(AsyncType[str]):
    name = "disk"

    async def async_convert(
        self,
        root: Root,
        value: str,
        param: Optional[click.Parameter],
        ctx: Optional[click.Context],
    ) -> str:
        return value

    async def async_complete(
        self, root: Root, ctx: click.Context, args: Sequence[str], incomplete: str
    ) -> List[Tuple[str, Optional[str]]]:
        async with await root.init_client() as client:
            ret: List[Tuple[str, Optional[str]]] = []
            async with client.service_accounts.list() as it:
                async for account in it:
                    account_name = account.name or ""
                    for test in (
                        account.id,
                        account_name,
                    ):
                        if test.startswith(incomplete):
                            ret.append((test, account_name))

            return ret


SERVICE_ACCOUNT = ServiceAccountType()
