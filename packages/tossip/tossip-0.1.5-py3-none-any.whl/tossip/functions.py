import subprocess

def getConnectedDeviceUDIDs():

    p = subprocess.Popen(["idveice_id", "-l"], stdout=subprocess.PIPE, shell=True)

    (output, err) = p.communicate

    p_status = p.wait()

    return output