""" module:: uds.common
    :platform: Posix
    :synopsis: An abstraction of ISO 14229 UDS protocol
    moduleauthor:: Patrick Menschel (menschel.p@posteo.de)
    license:: GPL v3
"""

import struct
from enum import IntEnum

import logging
from typing import Optional, List

LOGGER = logging.getLogger(__name__)


class DiagnosticSession(IntEnum):
    """
    Diagnostic session enum
    """
    DefaultSession = 1
    ProgrammingSession = 2
    ExtendedDiagnosticSession = 3
    SafetySystemDiagnosticSession = 4


class ResetType(IntEnum):
    """
    Reset type enum
    """
    HardReset = 1
    KeyOffOnReset = 2
    SoftReset = 3
    EnableRapidPowerShutdown = 4
    DisableRapidPowerShutdown = 5


class ComCtrlType(IntEnum):
    """
    Control types used in Communication Control service
    """
    EnableRxTx = 0
    EnableRxDisableTx = 1
    DisableRxEnableTx = 2
    DisableRxTx = 3
    EnableRxDisableTxEnhancedAddressInfo = 4
    EnableRxTxEnhancedAddressInfo = 5


class DtcSettingType(IntEnum):
    """
    Type used in uds service control dtc settings.
    """
    On = 1
    Off = 2


class ServiceId(IntEnum):
    """
    Service id enum
    """
    # Diagnostic and Communication Management
    DiagnosticSessionControl = 0x10
    EcuReset = 0x11
    SecurityAccess = 0x27
    CommunicationControl = 0x28
    TesterPresent = 0x3E
    AccessTimingParameter = 0x83
    SecuredDataTransmission = 0x84
    ControlDtcSettings = 0x85
    ResponseOnEvent = 0x86
    LinkControl = 0x87

    # Data Transmission
    ReadDataByIdentifier = 0x22
    ReadMemoryByAddress = 0x23
    ReadScalingDataByIdentifier = 0x24
    ReadDataByPeriodicIdentifier = 0x2A
    DynamicallyDefineDataIdentifier = 0x2C
    WriteDataByIdentifier = 0x2E
    WriteMemoryByAddress = 0x3D

    # Stored Data Transmission
    ClearDiagnosticInformation = 0x14
    ReadDtcInformation = 0x19

    # Input / Output Control
    InputOutputByIdentifier = 0x2F

    # Remote Activation of Routine
    RoutineControl = 0x31

    # Upload / Download
    RequestDownload = 0x34
    RequestUpload = 0x35
    DataTransfer = 0x36
    RequestTransferExit = 0x37


class ResponseCode(IntEnum):
    """
    UDS Negative Response Codes

    Some Explanation, when ISO14229 (UDS) was made,
    it had to be compatible with the preceding ISO14230 (KWP2000)
    so everything up to the 0x40 range is nearly identical.
    BTW: See how BOSCH managed to fake the ISO numbering?
    There are some unofficial ranges for different topics
    0x10-0x1F, 0x20-0x2F and so on.
    """
    # tester side error
    GeneralReject = 0x10
    ServiceNotSupported = 0x11
    SubFunctionNotSupported = 0x12
    IncorrectMessageLengthOrInvalidFormat = 0x13
    ResponseTooLong = 0x14

    # device side error
    BusyRepeatRequest = 0x21
    ConditionsNotCorrect = 0x22
    RequestSequenceError = 0x24
    NoResponseFromSubnetComponent = 0x25
    FaultPreventsExecutionOfRequestedAction = 0x26

    # function side error
    RequestOutOfRange = 0x31
    SecurityAccessDenied = 0x33
    InvalidKey = 0x35
    ExceededNumberOfAttempts = 0x36
    RequiredTimeDelayNotExpired = 0x37

    # 0x38-0x4F Reserved by Extended Data Link Security Document

    UploadDownloadNotAccepted = 0x70
    TransferDataSuspended = 0x71
    GeneralProgrammingFailure = 0x72
    WrongBlockSequenceCounter = 0x73

    RequestCorrectlyReceivedButResponsePending = 0x78
    # This is essentially not an Error, it is just a delay information.
    # This Response Code is due to the fact that standard autosar modules do not necessarily run on the same time disc
    # and no IPC method has every been defined for Autosar.

    SubFunctionNotSupportedInActiveSession = 0x7E
    ServiceNotSupportedInActiveSession = 0x7F


# parser and concat functions for services

def concat_diagnostic_session_control_request(session: DiagnosticSession) -> bytes:
    """
    Concat diagnostic session control request
    :param session: The requested diagnostic session.
    :return: The request as bytes.
    """
    assert session in DiagnosticSession
    return struct.pack("BB", ServiceId.DiagnosticSessionControl, session)


def parse_diagnostic_session_control_response(resp: bytes) -> dict:
    """
    Parse diagnostic session control response
    :param resp: The response message in bytes.
    :return: A dictionary with response specific values.
    """
    values = list(struct.unpack(">BBHH", resp))
    # scale both values to seconds
    values[1] = DiagnosticSession(values[1])
    values[2] = values[2] / 1000
    values[3] = values[3] / 100
    return dict(zip(["response_sid", "session", "p2_server_max", "p2*_server_max"], values))


def concat_ecu_reset_request(rtype: ResetType) -> bytes:
    """
    Concat ecu reset request
    :param rtype: The requested ResetType.
    :return: The request as bytes.
    """
    assert rtype in ResetType
    return struct.pack("BB", ServiceId.EcuReset, rtype)


def parse_ecu_reset_response(resp: bytes) -> dict:
    """
    Parse ecu reset response
    :param resp: The response message in bytes.
    :return: A dictionary with response specific values.
    """
    return dict(zip(["response_sid", "rtype", "power_down_time"], resp))


def concat_security_access_request(slevel: int,
                                   key: Optional[bytes]
                                   ) -> bytes:
    """
    Concat security access request
    :param slevel: The security level. Uneven=SeedRequest, Even=KeyPost
    :param key: The key bytes.
    :return: The request as bytes.
    """
    if slevel not in range(0x100):
        raise ValueError("Value {0} is not in range 0-0xFF".format(slevel))

    if (slevel & 0x1) == 0:
        if key is None:
            raise ValueError("Security Access to an even slevel ({0}) must provide a key {1}".format(slevel, key))
        req = struct.pack("BB{0}s".format(len(key)), ServiceId.SecurityAccess, slevel, key)
    else:
        req = struct.pack("BB", ServiceId.SecurityAccess, slevel)
    return req


def parse_security_access_response(resp: bytes) -> dict:
    """
    Parse security access response
    :param resp: The response message in bytes.
    :return: A dictionary with response specific values.
    """
    if resp[1] & 0x1:
        # response to seed request, so extract seed, otherwise not
        fmt = "BB{0}s".format(len(resp) - 2)
    else:
        fmt = "BB"
    values = list(struct.unpack(fmt, resp))
    keys = ["response_sid", "slevel", "seed"]
    return dict(zip(keys, values))


def concat_read_data_by_id_request(did: int) -> bytes:
    """
    Concat read data by id request
    :param did: The diagnostic identifier to be read.
    :return: The request as bytes.
    """
    if did not in range(0x10000):
        raise ValueError("Value {0} is not in range 0-0xFFFF".format(did))
    return struct.pack(">BH", ServiceId.ReadDataByIdentifier, did)


def parse_read_data_by_id_response(resp: bytes) -> dict:
    """
    Parse read data by id response
    :param resp: The response message in bytes.
    :return: A dictionary with response specific values.
    """
    return dict(zip(["response_sid", "did", "data"], struct.unpack(">BH{0}s".format(len(resp) - 3), resp)))


def concat_communication_control_request(ctrl_type: ComCtrlType,
                                         com_type: int,
                                         node_id: int,
                                         no_ack: bool = False,
                                         ) -> bytes:
    """
    Concat communication control request
    :param ctrl_type: The control type.
    :param com_type: The communication type.
    :param node_id: The Node identification number.
    :param no_ack: Suppress the the positive response.
    :return: The request as bytes.
    """
    assert ctrl_type in ComCtrlType
    if no_ack:
        ctrl_type_byte = ctrl_type | 0x80
    else:
        ctrl_type_byte = ctrl_type

    return struct.pack(">BBBH", ServiceId.CommunicationControl, ctrl_type_byte, com_type, node_id)


def parse_communication_control_response(resp: bytes) -> dict:
    """
    Parse communication control response
    :param resp: The response message in bytes.
    :return: A dictionary with response specific values.
    """
    values = list(struct.unpack("BB", resp))
    if values[1] & 0x80:
        raise ValueError("The suppress positive response bit is set, this is impossible")
    values[1] = ComCtrlType(values[1] & 0x7F)
    return dict(zip(["response_sid", "ctrl_type"], values))


# Todo: Authentication Request here - but its way to complicated for a beta, add when first non-beta release is out.


def concat_tester_present_request(no_ack: bool = False,
                                  ) -> bytes:
    """
    Concat tester present request
    :param no_ack: Suppress the the positive response.
    :return: The request as bytes.
    """
    zerosubfunction = 0
    if no_ack:
        zerosubfunction = 0x80
    return struct.pack("BB", ServiceId.TesterPresent, zerosubfunction)


def parse_tester_present_response(resp: bytes) -> dict:
    """
    Parse tester present response
    :param resp: The response message in bytes.
    :return: A dictionary with response specific values.
    """
    # second byte zerosubfunction is always 0
    return dict(zip(["response_sid", "zerosubfunction"], resp))


def concat_control_dtc_setting_request(stype: DtcSettingType,
                                       dtcs: Optional[List[int]] = None):
    """
    Concat control dtc setting request
    :param stype: The DtcSettingType On or Off
    :param dtcs: A list of dtc numbers in range 0-0xFFFF
    :return: The request as bytes.
    """

    if dtcs is not None:
        return struct.pack(">BB{0}H".format(len(dtcs)), ServiceId.ControlDtcSettings, stype, *dtcs)
    else:
        return struct.pack("BB", ServiceId.ControlDtcSettings, stype)


def parse_control_dtc_setting_response(resp: bytes) -> dict:
    """
    Parse control dtc setting response
    :param resp: The response message in bytes.
    :return: A dictionary with response specific values.
    """
    # second byte zerosubfunction is always 0
    values = list(resp)
    values[1] = DtcSettingType(values[1])
    return dict(zip(["response_sid", "stype"], values))


SERVICE_TO_PARSER_MAPPING = {ServiceId.DiagnosticSessionControl: parse_diagnostic_session_control_response,
                             ServiceId.EcuReset: parse_ecu_reset_response,
                             ServiceId.ReadDataByIdentifier: parse_read_data_by_id_response,
                             ServiceId.SecurityAccess: parse_security_access_response,
                             ServiceId.CommunicationControl: parse_communication_control_response,
                             ServiceId.TesterPresent: parse_tester_present_response,
                             ServiceId.ControlDtcSettings: parse_control_dtc_setting_response,

                             }


def parse_response(resp: bytes) -> dict:
    """
    A generic function to parse a service response.
    In case of negative response, it raises the appropriate protocol exceptions.
    Otherwise it calls a service specific parser and returns a dictionary with the contents.
    The UDS protocol was not designed properly, so the request is also needed to process the response.
    :param resp: The response bytes.
    :return: A dictionary with response specific values.
    """
    raise_for_exception(resp=resp)
    sid = ServiceId(resp[0] & 0xBF)
    parser_function = SERVICE_TO_PARSER_MAPPING.get(sid)
    ret = {"raw": resp}
    if parser_function is not None and callable(parser_function):
        ret.update(parser_function(resp))
    return ret


def raise_for_exception(resp: bytes) -> None:
    """
    In case of negative response, raise the appropriate protocol exceptions.
    :param resp: The response bytes.
    :return: Nothing.
    """

    if resp[0] == 0x7F:
        assert len(resp) >= 3
        assert resp[0] == 0x7F
        sid = ServiceId(resp[1])
        response_code = ResponseCode(resp[2])
        LOGGER.error("Service {0} Exception {1}".format(sid.name, response_code.name))
        raise RESPONSE_CODE_TO_EXCEPTION_MAPPING.get(response_code)


# Exceptions from client perspective

class UdsProtocolException(Exception):
    """
    The base exception for UDS
    """
    pass


class UdsTimeoutError(UdsProtocolException):
    """
    A (socket/message/protocol) timeout
    """
    pass


class NegativeResponse(UdsProtocolException):
    """
    The base negative response exception
    """
    pass


class GeneralReject(NegativeResponse):
    """
    Protocol specific exception
    """
    pass


class ServiceNotSupported(NegativeResponse):
    """
    Protocol specific exception
    """
    pass


class SubfunctionNotSupported(NegativeResponse):
    """
    Protocol specific exception
    """
    pass


class IncorrectMessageLengthOrInvalidFormat(NegativeResponse):
    """
    Protocol specific exception
    """
    pass


class ResponseTooLong(NegativeResponse):
    """
    Protocol specific exception
    """
    pass


class BusyRepeatRequest(NegativeResponse):
    """
    Protocol specific exception
    """
    pass


class ConditionsNotCorrect(NegativeResponse):
    """
    Protocol specific exception
    """
    pass


class RequestSequenceError(NegativeResponse):
    """
    Protocol specific exception
    """
    pass


class NoResponseFromSubnetComponent(NegativeResponse):
    """
    Protocol specific exception
    """
    pass


class FaultPreventsExecutionOfRequestedAction(NegativeResponse):
    """
    Protocol specific exception
    """
    pass


class RequestOutOfRange(NegativeResponse):
    """
    Protocol specific exception
    """
    pass


class SecurityAccessDenied(NegativeResponse):
    """
    Protocol specific exception
    """
    pass


class InvalidKey(NegativeResponse):
    """
    Protocol specific exception
    """
    pass


class ExceededNumberOfAttempts(NegativeResponse):
    """
    Protocol specific exception
    """
    pass


class RequiredTimeDelayNotExpired(NegativeResponse):
    """
    Protocol specific exception
    """
    pass


class UploadDownloadNotAccepted(NegativeResponse):
    """
    Protocol specific exception
    """
    pass


class TransferDataSuspended(NegativeResponse):
    """
    Protocol specific exception
    """
    pass


class GeneralProgrammingFailure(NegativeResponse):
    """
    Protocol specific exception
    """
    pass


class WrongBlockSequenceCounter(NegativeResponse):
    """
    Protocol specific exception
    """
    pass


class RequestCorrectlyReceivedButResponsePending(NegativeResponse):
    # This is actually not a Negative Response, see how we can handle this in program flow,
    # maybe base on Exception instead.
    """
    Protocol specific exception
    """
    pass


class SubFunctionNotSupportedInActiveSession(NegativeResponse):
    """
    Protocol specific exception
    """
    pass


class ServiceNotSupportedInActiveSession(NegativeResponse):
    """
    Protocol specific exception
    """
    pass


RESPONSE_CODE_TO_EXCEPTION_MAPPING = {
    ResponseCode.GeneralReject: GeneralReject,
    ResponseCode.ServiceNotSupported: ServiceNotSupported,
    ResponseCode.SubFunctionNotSupported: SubfunctionNotSupported,
    ResponseCode.IncorrectMessageLengthOrInvalidFormat: IncorrectMessageLengthOrInvalidFormat,
    ResponseCode.ResponseTooLong: ResponseTooLong,
    ResponseCode.BusyRepeatRequest: BusyRepeatRequest,
    ResponseCode.ConditionsNotCorrect: ConditionsNotCorrect,
    ResponseCode.RequestSequenceError: RequestSequenceError,
    ResponseCode.NoResponseFromSubnetComponent: NoResponseFromSubnetComponent,
    ResponseCode.FaultPreventsExecutionOfRequestedAction: FaultPreventsExecutionOfRequestedAction,
    ResponseCode.RequestOutOfRange: RequestOutOfRange,
    ResponseCode.SecurityAccessDenied: SecurityAccessDenied,
    ResponseCode.InvalidKey: InvalidKey,
    ResponseCode.ExceededNumberOfAttempts: ExceededNumberOfAttempts,
    ResponseCode.RequiredTimeDelayNotExpired: RequiredTimeDelayNotExpired,
    ResponseCode.UploadDownloadNotAccepted: UploadDownloadNotAccepted,
    ResponseCode.TransferDataSuspended: TransferDataSuspended,
    ResponseCode.GeneralProgrammingFailure: GeneralProgrammingFailure,
    ResponseCode.WrongBlockSequenceCounter: WrongBlockSequenceCounter,
    ResponseCode.RequestCorrectlyReceivedButResponsePending: RequestCorrectlyReceivedButResponsePending,
    ResponseCode.SubFunctionNotSupportedInActiveSession: SubFunctionNotSupportedInActiveSession,
    ResponseCode.ServiceNotSupportedInActiveSession: ServiceNotSupportedInActiveSession,
}
