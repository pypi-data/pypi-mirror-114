#
#   Tossip Library
#   A library to easily communicate with iOS Devices.
#
#   Copyright (C) 2021, LiquidDevelopmentNET
#   MIT License
#

from enum import Enum
from os import stat

def customRequest(service, args):

    """
    Executes a custom request to the libimobiledevice library.

    See https://www.quamotion.mobi/docs/imobiledevice/tools/

    :param service: Name of the service (e.g. "idevice_id")
    :param args: Args of the request (e.g. ["-l"])

    :return: The response in bytes
    """

    import subprocess

    p = subprocess.Popen(['.\\bin\\'+service]+args, stdout=subprocess.PIPE, shell=True)

    (output, err) = p.communicate()

    return output

def getConnectedDeviceUDIDs():

    """
    Get the UDID's of the iOS Devices are connected.

    :return: Array of the UDID's
    """

    import subprocess

    p = subprocess.Popen(['.\\bin\\idevice_id', '-l'], stdout=subprocess.PIPE, shell=True)

    (output, err) = p.communicate()

    udids = output.decode().replace('\r', '').split('\n')

    del udids[-1]

    return udids

def validatePairing(udid = None):

    """
    Get the PairingStatus of an iOS Device

    :param udid: OPTIONAL the udid of the iOS Device requested
    :return: PairingStatus the status of the pairing
    """

    import subprocess

    p = None

    if udid == None:
        p = subprocess.Popen(['.\\bin\\idevicepair', 'validate'], stdout=subprocess.PIPE, shell=True)
    else:
        p = subprocess.Popen(['.\\bin\\idevicepair', '-u', udid, 'validate'], stdout=subprocess.PIPE, shell=True)    

    (output, err) = p.communicate()

    status = PairingStatus.NONE
    decodedOutput = output.decode()

    if "SUCCESS:" in decodedOutput:
        status = PairingStatus.IS_PAIRED
    elif "ERROR:" in decodedOutput:
        status = PairingStatus.PLEASE_ACCEPT_DIALOGUE
    else:
        raise Exception(decodedOutput)

    return status

class PairingStatus(Enum):
    PLEASE_ACCEPT_DIALOGUE = 0
    IS_PAIRED = 1
    NONE = 2

def pair(udid = None):

    """
    Pair with an iOS Device

    :param udid: OPTIONAL the udid of the iOS Device requested
    :return: PairingStatus the status of the pairing
    """

    import subprocess

    p = None

    if udid == None:
        p = subprocess.Popen(['.\\bin\\idevicepair', 'pair'], stdout=subprocess.PIPE, shell=True)
    else:
        p = subprocess.Popen(['.\\bin\\idevicepair', '-u', udid, 'pair'], stdout=subprocess.PIPE, shell=True)    

    (output, err) = p.communicate()

    status = PairingStatus.NONE
    decodedOutput = output.decode()

    if "SUCCESS:" in decodedOutput:
        status = PairingStatus.IS_PAIRED
    elif "ERROR:" in decodedOutput:
        status = PairingStatus.PLEASE_ACCEPT_DIALOGUE
    else:
        raise Exception(decodedOutput)

    return status    

def unpair(udid = None):

    """
    Unpair an iOS Device

    :param udid: OPTIONAL the udid of the iOS Device requested
    :return: boolean if the operation was successful
    """

    import subprocess

    p = None

    if udid == None:
        p = subprocess.Popen(['.\\bin\\idevicepair', 'unpair'], stdout=subprocess.PIPE, shell=True)
    else:
        p = subprocess.Popen(['.\\bin\\idevicepair', '-u', udid, 'unpair'], stdout=subprocess.PIPE, shell=True)    

    (output, err) = p.communicate()

    status = PairingStatus.NONE
    decodedOutput = output.decode()

    if "SUCCESS:" in decodedOutput:
        return True
    else:
        raise Exception(decodedOutput)
