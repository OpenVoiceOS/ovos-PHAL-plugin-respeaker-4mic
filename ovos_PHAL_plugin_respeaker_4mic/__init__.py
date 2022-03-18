from gpiozero import LED
from pixel_ring import pixel_ring
from time import sleep

from ovos_PHAL.detection import is_respeaker_4mic
from ovos_plugin_manager.phal import PHALPlugin


class Respeaker4MicValidator:
    @staticmethod
    def validate(config=None):
        # TODO does it work for 2 and 6 mic ?
        return is_respeaker_4mic()


class Respeaker4MicControlPlugin(PHALPlugin):
    def __init__(self, bus=None, config=None):
        super().__init__(bus=bus, name="ovos-PHAL-plugin-respeaker-4mic", config=config)
        self.power = LED(5)
        self.power.on()
        pixel_ring.set_brightness(10)
        pixel_ring.change_pattern('echo')
        pixel_ring.wakeup()
        sleep(1.5)
        pixel_ring.off()

    def on_record_begin(self, message=None):
        pixel_ring.listen()

    def on_record_end(self, message=None):
        self.on_reset(message)

    def on_audio_output_start(self, message=None):
        pixel_ring.speak()

    def on_audio_output_end(self, message=None):
        self.on_reset(message)

    def on_think(self, message=None):
        pixel_ring.think()

    def on_reset(self, message=None):
        pixel_ring.off()

    def on_system_reset(self, message=None):
        self.on_reset(message)

    def shutdown(self):
        pixel_ring.off()
        self.power.off()
        super().shutdown()
