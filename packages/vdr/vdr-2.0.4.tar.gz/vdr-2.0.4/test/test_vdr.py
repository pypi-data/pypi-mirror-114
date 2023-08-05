import vdr

VDR = vdr.Vdr()
VDR.add_connection("localhost", 12345, "ecdis")
VDR.add_connection("localhost", 12346, "radar")
VDR.add_connection("localhost", 12347, "nmea")
VDR.add_connection("localhost", 12348, "sound_bridge")

ECDIS = vdr.ReceivingFrame(VDR, "ecdis")
RADAR = vdr.ReceivingFrame(VDR, "radar")
NMEA = vdr.ReceivingNmea(VDR, "nmea")
SOUND_BRIDGE = vdr.ReceivingVoice(VDR, "sound_bridge")

ECDIS.start()
RADAR.start()
NMEA.start()
SOUND_BRIDGE.start()
