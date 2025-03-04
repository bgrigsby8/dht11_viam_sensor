import adafruit_dht
import board
from typing import (Any, ClassVar, Dict, Final, List, Mapping, Optional,
                    Sequence)

from typing_extensions import Self
from viam.components.sensor import *
from viam.logging import getLogger
from viam.proto.app.robot import ComponentConfig
from viam.proto.common import Geometry, ResourceName
from viam.resource.base import ResourceBase
from viam.resource.easy_resource import EasyResource
from viam.resource.types import Model, ModelFamily
from viam.utils import SensorReading, ValueTypes, struct_to_dict

LOGGER = getLogger(__name__)

class Humidity(Sensor, EasyResource):
    MODEL: ClassVar[Model] = Model(ModelFamily("brad-grigsby", "dht11"), "humidity")

    @classmethod
    def new(
        cls, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]
    ) -> Self:
        """This method creates a new instance of this Sensor component.
        The default implementation sets the name from the `config` parameter and then calls `reconfigure`.

        Args:
            config (ComponentConfig): The configuration for this resource
            dependencies (Mapping[ResourceName, ResourceBase]): The dependencies (both implicit and explicit)

        Returns:
            Self: The resource
        """
        return super().new(config, dependencies)

    @classmethod
    def validate_config(cls, config: ComponentConfig) -> Sequence[str]:
        """This method allows you to validate the configuration object received from the machine,
        as well as to return any implicit dependencies based on that `config`.

        Args:
            config (ComponentConfig): The configuration for this resource

        Returns:
            Sequence[str]: A list of implicit dependencies
        """
        attributes = struct_to_dict(config.attributes)
        if "pin" not in attributes:
            raise Exception("Missing 'pin' attribute in config")
        
        return []

    def reconfigure(
        self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]
    ):
        """This method allows you to dynamically update your service when it receives a new `config` object.

        Args:
            config (ComponentConfig): The new configuration
            dependencies (Mapping[ResourceName, ResourceBase]): Any dependencies (both implicit and explicit)
        """
        attributes = struct_to_dict(config.attributes)

        # Map the pin number to the corresponding pin on the Raspberry Pi
        pin_map = {
            3: board.D2,
            5: board.D3,
            7: board.D4,
            8: board.D14,
            10: board.D15,
            11: board.D17,
            12: board.D18,
            13: board.D27,
            15: board.D22,
            16: board.D23,
            18: board.D24,
            19: board.D10,
            21: board.D9,
            22: board.D25,
            23: board.D11,
            24: board.D8,
            26: board.D7,
            29: board.D5,
            31: board.D6,
            32: board.D12,
            33: board.D13,
            35: board.D19,
            36: board.D16,
            37: board.D26,
            38: board.D20,
            40: board.D21,
        }

        pin_number = attributes["pin"]
        if pin_number in pin_map:
            gpio_number = pin_map[pin_number]
        else:
            raise Exception(f"Invalid pin number: {pin_number}")
        
        self.dht_device = adafruit_dht.DHT11(gpio_number)

        return super().reconfigure(config, dependencies)

    async def get_readings(
        self,
        *,
        extra: Optional[Mapping[str, Any]] = None,
        timeout: Optional[float] = None,
        **kwargs
    ) -> Mapping[str, SensorReading]:
        humidity = self.dht_device.humidity

        if humidity is not None:
            return {"Humidity %": humidity}
        else:
            raise Exception("Failed to read DHT11 sensor")

    async def do_command(
        self,
        command: Mapping[str, ValueTypes],
        *,
        timeout: Optional[float] = None,
        **kwargs
    ) -> Mapping[str, ValueTypes]:
        raise NotImplementedError()

    async def get_geometries(
        self, *, extra: Optional[Dict[str, Any]] = None, timeout: Optional[float] = None
    ) -> List[Geometry]:
        raise NotImplementedError()

