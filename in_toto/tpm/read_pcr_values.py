"""
<Program Name>
  read_pcr_values.py

<Author>
  Ashish Das <ashish.das@nyu.edu>

<Started>
  April 27, 2020

<Copyright>
  See LICENSE for licensing information.

<Purpose>
  Provides a wrapper to read the pcr values of the TPM present on the machine.

  The wrapper performs the following tasks.

    - Checks if there is a TPM version 2.0 is present on the machine.
    - Records the current PCR values of the machine's TPM
    - Returns a list of PCR values for either one hash algorithm, or for all
      the algorithms.

"""
import subprocess
import os

def is_tpm2():
    """
    <Purpose>
      A function which checks for the presence of TPM2.0 
      (hardware/virtual) on the machine.
    <Arguments>
      None
    <Exceptions>
      Returns an exception when there is no TPM2.0 detected on the machine.
    <Returns>
      Bool value

    """
    if os.path.exists("/dev/tpmrm0"):
        #TODO: This is currently a trivial way of testing for TPM2.0. 
        #Beginning with kernel 5.6 we can simply read 
        #the "/sys/class/tpm/tpm0/tpm_version_major" attribute.
        return True
    else:
        raise Exception(
            "TPM2.0 not present on the machine")

def read_pcrs():
    """
    <Purpose>
      A function which reads the pcr values of the tpm present on the machine 
      with the help of tpm2-tools library command "tpm2_pcrread". If the 
      command runs, it stores the values of the sha256 PCR stack in a list.
    <Arguments>
      None
    <Exceptions>
      None
    <Returns>
      A list containing the sha256 PCR values.

    """
    if is_tpm2():
        res = subprocess.run(["tpm2_pcrread", "sha256:all"], stdout= subprocess.PIPE)
        res.check_returncode()
        pcrs = res.stdout
        pcrs = str(pcrs, 'utf-8').split('\n')
        return pcrs
    else:
        raise Exception(
                "Could not read the PCRs, please check the command")
