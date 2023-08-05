from enum import IntEnum
from nmigen import unsigned
from naps import packed_struct

__all__ = ["DsiShortPacketDataType", "DsiLongPacketDataType", "DsiErrorResponse"]


class DsiShortPacketDataType(IntEnum):
    V_SYNC_START = 0x01
    V_SYNC_END = 0x11
    H_SYNC_START = 0x21
    H_SYNC_END = 0x31
    END_OF_TRANSMISSION_PACKET = 0x08
    COLOR_MODE_OFF = 0x02
    COLOR_MODE_ON = 0x12
    SHUT_DOWN_PERIPHERAL = 0x22
    TURN_ON_PERIPHERAL = 0x32
    GENERIC_SHORT_WRITE_0_PARAMETER = 0x03
    GENERIC_SHORT_WRITE_1_PARAMETER = 0x13
    GENERIC_SHORT_WRITE_2_PARAMETER = 0x23
    GENERIC_READ_0_PARAMETER = 0x04
    GENERIC_READ_1_PARAMETER = 0x14
    GENERIC_READ_2_PARAMETER = 0x24
    DCS_SHORT_WRITE_0_PARAMETER = 0x05
    DCS_SHORT_WRITE_1_PARAMETER = 0x15
    DCS_READ_0_PARAMETER = 0x06
    SET_MAXIMUM_RETURN_PACKET_SIZE = 0x37


class DsiLongPacketDataType(IntEnum):
    NULL_PACKET_NO_DATA = 0x09
    BLANKING_PACKET_NO_DATA = 0x19
    GENERIC_LONG_WRITE = 0x29
    DCS_LONG_WRITE = 0x39
    LOOSELY_PACKET_PIXEL_STREAM_20_BIT_YCBCR_4_2_2 = 0x0C
    PACKED_PIXEL_STREAM_24_BIT_YCBCR_4_2_2 = 0x1C
    PACKED_PIXEL_STREAM_16_BIT_YCBCR_4_2_2 = 0x2C
    PACKED_PIXEL_STREAM_30_BIT_RGB_10_10_10 = 0x0D
    PACKED_PIXEL_STREAM_36_BIT_RGB_12_12_12 = 0x1D
    PACKED_PIXEL_STREAM_12_BIT_YCBCR_4_2_0 = 0x3D
    PACKED_PIXEL_STREAM_16_BIT_RGB_5_6_5 = 0x0E
    PACKED_PIXEL_STREAM_18_BIT_RGB_6_6_6 = 0x1E
    LOOSELY_PACKET_PIXEL_STREAM_18_BIT_RGB_6_6_6 = 0x2E
    PACKED_PIXEL_STREAM_24_BIT_RGB_8_8_8 = 0x3E

@packed_struct
class DsiErrorResponse:
    SOT_ERROR: unsigned(1)
    SOT_SYNC_ERROR: unsigned(1)
    EOT_SYNC_ERROR: unsigned(1)
    ESCAPE_MODE_ENTRY_COMMAND_ERROR: unsigned(1)
    LOW_POWER_TRANSMIT_SYNC_ERROR: unsigned(1)
    PERIPHERAL_TIMEOUT_ERROR: unsigned(1)
    FALSE_CONTROL_ERROR: unsigned(1)
    CONTENTION_DETECTED: unsigned(1)
    ECC_ERROR_SINGLE_BIT_CORRECTED: unsigned(1)
    ECC_ERROR_MULTI_BIT_NOT_CORRECTED: unsigned(1)
    CHECKSUM_ERROR: unsigned(1)
    DSI_DATA_TYPE_NOT_RECOGNIZED: unsigned(1)
    DSI_VC_ID_INVALID: unsigned(1)
    INVALID_TRANSMISSION_LENGTH: unsigned(1)
    RESERVED: unsigned(1)
    DSI_PROTOCOL_VIOLATION: unsigned(1)