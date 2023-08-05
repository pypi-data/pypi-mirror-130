"""
Module for entities implemented using the
button platform (https://www.home-assistant.io/integrations/button/).
"""
from __future__ import annotations

import logging

from hahomematic.const import HmPlatform
from hahomematic.entity import BaseParameterEntity

_LOGGER = logging.getLogger(__name__)


class HmButton(BaseParameterEntity):
    """
    Implementation of a button.
    This is a default platform that gets automatically generated.
    """

    def __init__(self, device, unique_id, address, parameter, parameter_data):
        super().__init__(
            device=device,
            unique_id=unique_id,
            address=address,
            parameter=parameter,
            parameter_data=parameter_data,
            platform=HmPlatform.BUTTON,
        )

    async def press(self) -> None:
        """Handle the button press."""
        await self.send_value(True)
