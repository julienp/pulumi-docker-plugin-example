import argparse
import asyncio
import sys
from typing import Optional

import grpc
import grpc.aio
from pulumi.provider import Provider
from pulumi.provider.experimental.provider import ComponentProvider
from pulumi.provider.server import ProviderServicer
from pulumi.resource import ComponentResource
from pulumi.runtime.proto import provider_pb2_grpc

from component import Greeter

is_hosting = False


_MAX_RPC_MESSAGE_SIZE = 1024 * 1024 * 400
_GRPC_CHANNEL_OPTIONS = [("grpc.max_receive_message_length", _MAX_RPC_MESSAGE_SIZE)]


def main(provider: Provider, args: list[str]) -> None:  # args not in use?
    """For use as the `main` in programs that wrap a custom Provider
    implementation into a Pulumi-compatible gRPC server.

    :param provider: an instance of a Provider subclass

    :args: command line arguiments such as os.argv[1:]

    """

    argp = argparse.ArgumentParser(description="Pulumi provider plugin (gRPC server)")
    argp.add_argument("engine", help="Pulumi engine address")
    argp.add_argument("--logflow", action="store_true", help="Currently ignored")
    argp.add_argument("--logtostderr", action="store_true", help="Currently ignored")

    known_args, _ = argp.parse_known_args()
    engine_address: str = known_args.engine

    async def serve() -> None:
        server = grpc.aio.server(options=_GRPC_CHANNEL_OPTIONS)
        servicer = ProviderServicer(provider, args, engine_address=engine_address)
        provider_pb2_grpc.add_ResourceProviderServicer_to_server(servicer, server)
        port = server.add_insecure_port(address="127.0.0.1:4242")
        await server.start()
        sys.stdout.buffer.write(f"{port}\n".encode())
        sys.stdout.buffer.flush()
        await server.wait_for_termination()

    try:
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(serve())
        finally:
            loop.close()
    except KeyboardInterrupt:
        pass


def component_provider_host2(
    components: list[type[ComponentResource]],
    name: str,
    namespace: Optional[str] = None,
):
    """
    component_provider_host starts the provider and hosts the passed in components.
    The provider's schema is inferred from the type annotations of the components.
    See `analyzer.py` for more details.

    :param metadata: The metadata for the provider. If not provided, the name
    defaults to the plugin's directory name, and version defaults to "0.0.1".
    """
    global is_hosting  # noqa
    if is_hosting:
        # Bail out if we're already hosting. This prevents recursion when the
        # analyzer loads this file. It's usually good style to not run code at
        # import time, and use `if __name__ == "__main__"`, but let's make sure
        # we guard against this.
        return
    is_hosting = True

    # When the languge runtime runs the plugin, the first argument is the path
    # to the plugin's installation directory. This is followed by the engine
    # address and other optional arguments flags, like `--logtostderr`.
    args = sys.argv[1:]
    # Default the version to "0.0.0" for now, otherwise SDK codegen gets
    # confused without a version.
    version = "0.0.0"
    main(ComponentProvider(components, name, namespace, version), args)


if __name__ == "__main__":
    component_provider_host2(name="greeter", components=[Greeter])
