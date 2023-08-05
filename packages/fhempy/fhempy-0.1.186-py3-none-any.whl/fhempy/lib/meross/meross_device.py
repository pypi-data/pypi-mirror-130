import asyncio
from fhempy.lib.generic import FhemModule
from fhempy.lib import fhem, fhem_pythonbinding
from meross_iot.model.enums import OnlineStatus, Namespace
from meross_iot.controller.mixins.toggle import ToggleMixin, ToggleXMixin
from meross_iot.controller.mixins.garage import GarageOpenerMixin
from meross_iot.controller.mixins.light import LightMixin


class meross_device:
    def __init__(self, logger, fhemdevice: FhemModule):
        self.logger = logger
        self.fhemdev = fhemdevice
        self.hash = fhemdevice.hash

    async def Define(self, hash, args, argsh):
        self._setupdev_name = args[3]
        self._deviceid = args[4]
        self._device = None
        self.hash["DEVICEID"] = self._deviceid

        self._setupdev = None
        await fhem.readingsSingleUpdate(self.hash, "state", "ready", 1)
        self.fhemdev.create_async_task(self._init_device())

    async def _get_set_commands(self):
        set_conf = {}

        if isinstance(self._device, ToggleXMixin) or isinstance(
            self._device, ToggleMixin
        ):
            set_conf["on"] = {}
            set_conf["off"] = {}
            set_conf["toggle"] = {}

        if isinstance(self._device, GarageOpenerMixin):
            set_conf["open"] = {}
            set_conf["close"] = {}

        if isinstance(self._device, LightMixin):
            if self._device.get_supports_rgb():
                set_conf["rgb"] = {"args": ["value"], "options": "colorpicker,RGB"}
            if self._device.get_supports_luminance():
                set_conf["brightness"] = {
                    "args": ["value"],
                    "options": "colorpicker,BRI,0,1,100",
                }
            if self._device.get_supports_temperature():
                set_conf["ct"] = {
                    "args": ["value"],
                    "options": "colorpicker,CT,2000,1,6500",
                }

        self.fhemdev.set_set_config(set_conf)

    async def set_rgb(self, hash, params):
        rgb = params["value"]
        red = int(rgb[0:2], base=16)
        green = int(rgb[2:4], base=16)
        blue = int(rgb[4:6], base=16)
        await self._device.async_set_light_color(rgb=(red, green, blue))

    async def set_brightness(self, hash, params):
        bri = params["value"]
        await self._device.async_set_light_color(luminance=bri)

    async def set_ct(self, hash, params):
        ct = params["value"]
        await self._device.async_set_light_color(temperature=ct)

    async def set_on(self, hash, params):
        await self._device.async_turn_on()

    async def set_off(self, hash, params):
        await self._device.async_turn_off()

    async def set_toggle(self, hash, params):
        await self._device.async_toggle()

    async def set_open(self, hash, params):
        await self._device.async_open()

    async def set_close(self, hash, params):
        await self._device.async_close()

    async def _init_device(self):
        try:
            await self._connect_to_setup_device()
            await self._setup_device()
            await self._get_set_commands()
            await self.update_readings()
        except Exception as ex:
            self.logger.exception(ex)

    async def _connect_to_setup_device(self):
        while self._setupdev is None or self._setupdev.ready is False:
            await asyncio.sleep(1)
            self._setupdev = fhem_pythonbinding.getFhemPyDeviceByName(
                self._setupdev_name
            )
            if self._setupdev:
                self._setupdev = self._setupdev.meross_device

    async def _async_push_notification_received(
        self, namespace: Namespace, data: dict, device_internal_id: str
    ):
        update_state = False
        full_update = False

        if namespace == Namespace.CONTROL_UNBIND:
            self.logger.warning(
                f"Received unbind event. Removing device {self._device.name} from FHEM"
            )
            await self.platform.async_remove_entity(self.entity_id)
        elif namespace == Namespace.SYSTEM_ONLINE:
            self.logger.warning(f"Device {self._device.name} reported online event.")
            online = OnlineStatus(int(data.get("online").get("status")))
            update_state = True
            full_update = online == OnlineStatus.ONLINE

        elif namespace == Namespace.HUB_ONLINE:
            self.logger.warning(
                f"Device {self._device.name} reported (HUB) online event."
            )
            online = OnlineStatus(int(data.get("status")))
            update_state = True
            full_update = online == OnlineStatus.ONLINE
        else:
            update_state = True
            full_update = False

        if full_update:
            await self._device.async_update()

        if update_state:
            await self.update_readings()

    async def _setup_device(self):
        self._device = self._setupdev.get_device_by_id(self._deviceid)

        if self._device is not None:
            await self._device.async_update()
            self._device.register_push_notification_handler_coroutine(
                self._async_push_notification_received
            )

    async def update_readings(self):
        await fhem.readingsBeginUpdate(self.hash)
        await fhem.readingsBulkUpdateIfChanged(self.hash, "uuid", self._device.uuid)
        await fhem.readingsBulkUpdateIfChanged(self.hash, "name", self._device.name)
        await fhem.readingsBulkUpdateIfChanged(
            self.hash, "firmware_version", self._device.firmware_version
        )
        await fhem.readingsBulkUpdateIfChanged(
            self.hash, "hardware_version", self._device.hardware_version
        )
        await fhem.readingsBulkUpdateIfChanged(
            self.hash, "internal_id", self._device.internal_id
        )
        await fhem.readingsBulkUpdateIfChanged(
            self.hash, "mqtt_host", self._device.mqtt_host
        )
        await fhem.readingsBulkUpdateIfChanged(
            self.hash, "mqtt_port", self._device.mqtt_port
        )
        await fhem.readingsBulkUpdateIfChanged(self.hash, "type", self._device.type)
        await fhem.readingsBulkUpdateIfChanged(
            self.hash, "online_status", self._device.online_status.name
        )

        if isinstance(self._device, ToggleXMixin) or isinstance(
            self._device, ToggleMixin
        ):
            state_val = "off"
            if self._device.is_on():
                state_val = "on"

        if isinstance(self._device, GarageOpenerMixin):
            state_val = "closed"
            if self._device.get_is_open():
                state_val = "open"

        if isinstance(self._device, LightMixin):
            ct = self._device.get_color_temperature()
            await fhem.readingsBulkUpdateIfChanged(self.hash, "ct", ct)

            bri = self._device.get_luminance()
            await fhem.readingsBulkUpdateIfChanged(self.hash, "brightness", bri)

            rgb_tuple = self._device.get_rgb_color()
            rgb = f"{rgb_tuple[0]:02x}{rgb_tuple[1]:02x}{rgb_tuple[2]:02x}"
            await fhem.readingsBulkUpdateIfChanged(self.hash, "rgb", rgb)

        await fhem.readingsBulkUpdateIfChanged(self.hash, "state", state_val)
        await fhem.readingsEndUpdate(self.hash, 1)
