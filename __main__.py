from pulumi.provider.experimental import component_provider_host

from .component import Greeter

if __name__ == "__main__":
    component_provider_host(name="greeter", components=[Greeter])
