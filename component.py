from typing import Optional, TypedDict

import pulumi
import pulumi_random


class GreeterArgs(TypedDict):
    who: Optional[pulumi.Input[str]]


class Greeter(pulumi.ComponentResource):
    greeting: pulumi.Output[Optional[str]]

    def __init__(
        self,
        name: str,
        args: GreeterArgs,
        opts: Optional[pulumi.ResourceOptions] = None,
    ):
        super().__init__("cloudrun:index:Service", name, {}, opts)
        who = args.get("who") or "Pulumipus"
        greeting_word = pulumi_random.RandomShuffle(
            f"{name}-greeting",
            inputs=["Hello", "Bonjour", "Ciao", "Hola"],
            result_count=1,
            opts=pulumi.ResourceOptions(parent=self),
        )
        self.greeting = pulumi.Output.concat(greeting_word.results[0], ", ", who, "!")
        self.register_outputs({"greeting": self.greeting})
