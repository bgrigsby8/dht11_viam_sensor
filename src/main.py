import asyncio
from viam.module.module import Module
from .models.humidity import Humidity


if __name__ == '__main__':
    asyncio.run(Module.run_from_registry())
