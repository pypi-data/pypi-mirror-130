""" module:: uds.client
    :platform: Posix
    :synopsis: A class file for Universal Diagnostic Service (UDS) client
    moduleauthor:: Patrick Menschel (menschel.p@posteo.de)
    license:: GPL v3
"""

import datetime
import struct
from queue import Queue, Empty
from threading import Thread
from typing import Optional, List

from socketcan import CanIsoTpSocket

from uds.common import parse_response, ServiceId, UdsTimeoutError, DiagnosticSession, ResetType, \
    concat_diagnostic_session_control_request, concat_ecu_reset_request, concat_security_access_request, \
    concat_read_data_by_id_request, ComCtrlType, concat_communication_control_request, concat_tester_present_request, \
    concat_control_dtc_setting_request, DtcSettingType

import logging

LOGGER = logging.getLogger(__name__)


class UdsClient:
    """
    UDS Client class

    depends on socketcan
    therefore runs on linux only
    """

    def __init__(self,
                 socket: CanIsoTpSocket,
                 timeout: int = 5,
                 ):
        """
        Constructor

        :param socket: A SocketCAN IsoTp socket.
        """
        self._s = socket
        self.timeout = timeout
        self.rx_queue = Queue()
        self.rx_handler = Thread(target=self._handle_rx)
        self.rx_handler.setDaemon(True)
        self.rx_handler.start()

    # basic functionality

    def _handle_rx(self) -> None:
        """
        Puts data from socket into a queue,
        where the requester (main thread) in self.recv()
        :return: Nothing.
        """
        while True:
            self.rx_queue.put(self._s.recv())

    def _send(self, data: bytes) -> int:
        """
        Sends data to the socket.
        :param data: The data to be sent.
        :return: The length of data that was sent.
        """
        return self._s.send(data=data)

    def _recv(self) -> Optional[bytes]:
        """
        Receives data from rx_queue in case it was filled by
        rx_handler.
        The underlying queue mechanism may raise an Empty Exception.
        :return: Data bytes.
        """
        return self.rx_queue.get(timeout=self.timeout)

    def request(self, req: bytes) -> Optional[dict]:
        """
        Service request function
        It handles transmission, reception and check if a negative response error should be raised
        :param req: The request as bytes.
        :return: The response as bytes.
        :raises: Subtypes of NegativeResponse, UdsTimeoutError, etc.
        """
        bytes_sent = self._send(req)
        ts_request_sent = datetime.datetime.now()
        if bytes_sent != len(req):
            raise RuntimeError("bytes_sent != len(data)")
        try:
            resp = self._recv()
        except Empty:
            raise UdsTimeoutError
        else:
            time_for_response = datetime.datetime.now() - ts_request_sent
            LOGGER.debug("Response received after timedelta {0}".format(time_for_response))
            return parse_response(resp)

    # convenience functions for specific services

    def diagnostic_session_control(self,
                                   session: DiagnosticSession = DiagnosticSession.ExtendedDiagnosticSession) -> dict:
        """
        Basic uds service diagnostic session control.
        :param session: The requested diagnostic session.
        :return: The data that was returned.
        """
        return self.request(req=concat_diagnostic_session_control_request(session=session))

    def ecu_reset(self,
                  rtype: ResetType = ResetType.HardReset) -> dict:
        """
        Basic uds service ecu reset.
        :param rtype: The requested ResetType.
        :return: The data that was returned.
        """
        return self.request(req=concat_ecu_reset_request(rtype=rtype))

    def security_access(self,
                        slevel: int,
                        key: Optional[bytes] = None,
                        ) -> dict:
        """
        Basic uds service security access.
        The method is called SEED&KEY and was defined in KWP2000(ISO14230).
        The idea is to have a secret needed to compute a key from a given seed.
        In reality the seed/key is 4 bytes big endian and the seed2key function is a simple function,
        e.g. adding some value, rotating the seed, xor it with a mask value etc.

        Each security level is a tuple of an uneven number to request a seed
        and the next (even) number to post a key.
        :param slevel: The security level. Uneven=SeedRequest, Even=KeyPost
        :param key: The key bytes.
        :return: The data that was returned.
        """

        return self.request(req=concat_security_access_request(slevel=slevel,
                                                               key=key))

    def communication_control(self,
                              ctrl_type: ComCtrlType,
                              com_type: int,
                              node_id: int,
                              no_ack: bool = False) -> dict:
        """
        Basic uds service communication control.
        :param ctrl_type: The control type.
        :param com_type: The communication type.
        :param node_id: The Node identification number.
        :param no_ack: Suppress the the positive response.
        :return: The data that was returned.
        """
        return self.request(req=concat_communication_control_request(ctrl_type=ctrl_type,
                                                                     com_type=com_type,
                                                                     node_id=node_id,
                                                                     no_ack=no_ack))

    def tester_present(self,
                       no_ack: bool = False) -> dict:
        """
        Basic uds service tester present.
        :param no_ack: Suppress the the positive response.
        :return: The data that was returned. Actually nothing except for the response_sid.
        """
        return self.request(req=concat_tester_present_request(no_ack=no_ack))

    def control_dtc_setting(self,
                            stype: DtcSettingType,
                            dtcs: Optional[List[int]] = None):
        """
        Basic uds service control dtc setting.
        :param stype: The DtcSettingType On or Off
        :param dtcs: A list of dtc numbers in range 0-0xFFFF
        :return: The data that was returned.
        """
        return self.request(req=concat_control_dtc_setting_request(stype=stype, dtcs=dtcs))

    def read_data_by_id(self,
                        did: int) -> dict:
        """
        Basic uds service read data by id.
        :param did: The diagnostic identifier to be read.
        :return: The data that was returned.
        """
        return self.request(req=concat_read_data_by_id_request(did=did))
