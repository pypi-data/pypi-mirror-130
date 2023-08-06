# CDK Minecraft Server

Create an AWS hosted Minecraft server quick and easy within minutes!!

## Getting Started

```python
# Example automatically generated from non-compiling source. May contain errors.
import ckd_minecraft_server as mc_server

# Lookup VPC
vpc = ec2.Vpc.from_lookup(self, "my-default-vpc",
    vpc_name="my-default-vpc"
)

# Create Server
mc_server.MinecraftServer(self, "MyMCServer",
    vpc=vpc,
    game_server_name="MyServer",
    server_zip_path=path.join(__dirname, "./some/path/modpack.zip")
)
```
