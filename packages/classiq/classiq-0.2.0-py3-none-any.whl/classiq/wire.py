from typing import Optional

from classiq_interface.generator import function_call

from classiq.exceptions import ClassiqWiringError


class Wire:
    def __init__(
        self,
        start_call: Optional[function_call.FunctionCall] = None,
        output_name: str = "",
    ) -> None:
        self._start_call: function_call.FunctionCall = start_call
        self._start_name: str = output_name
        self._wire_name: str = ""
        if start_call is not None:
            self._wire_name = f"{start_call.name}_{self._start_name}"

        self._connected: bool = False

    def connect_wire(
        self, end_call: function_call.FunctionCall, input_name: str
    ) -> None:
        if self._start_call is None:
            raise ClassiqWiringError("Cannot connect one-sided wire")
        self._verify_and_update_connected()

        self._start_call.outputs[self._start_name] = self._wire_name
        end_call.inputs[input_name] = self._wire_name

    def _verify_and_update_connected(self) -> None:
        if self._connected:
            raise ClassiqWiringError("Wire already connected")

        self._connected = True
