from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import argparse
import os
import sys
from passwd_encrypt import __version__

VERSION = __version__
DATE = "22-Jul-2021"
AUTHOR = "Javier Ramos"
GITHUB = "https://github.com/jrdcasa"


# =============================================================================
def pw_print_header():
    """
    Print header
    """
    print("\n#############################################")
    print("#            PASSWD_ENCRYPT                 #")
    print("#           Dr. Javier Ramos                #")
    print("#    Macromolecular Physics Department      #")
    print("#              IEM-CSIC                     #")
    print("#       https://github.com/jrdcasa          #")
    print("#############################################")

    print(" Usage:")
    print(" passwd_encrypt [--createkeys|-c] <pattern>  # Generate the private and public keys "
          "as <pattern>.pem and <pattern>.pem.pub, respectively in the working directory.")
    print(" passwd_encrypt [--encrypt|-e] <rsa public key file> <message to encrypt>  "
          " # Encrypt message with the public key.")
    print(" passwd_encrypt [--decrypt|-d] <rsa private key file> <string or file containing "
          "the message to decrypt>  # Decrypt message with the public key.")
    print("")


# =============================================================================
def pw_parse_arguments():

    """
    Parse arguments of the CLI
    """

    # Create the parser
    cli_parser = argparse.ArgumentParser(description='Help to generate a encrypted/dencrypt file of a ssh password')
    group1 = cli_parser.add_mutually_exclusive_group()
    group1.add_argument("--usage", "-u", help="Print help and exit", action='store_true', default=False)
    group1.add_argument("--version", "-v", help="Version of the program", action='store_true', default=False)
    group1.add_argument("--createkeys", "-c", help="Create a pair of keys", action='store',
                        default=False, metavar='PATTERN')
    group1.add_argument("--encrypt", "-e", help="Encrypt the message using public key", action='store',
                        default=False, metavar=('PUBLIC_KEY_FILE', 'MESSAGE'), dest="encrypt", nargs=2)
    group1.add_argument("--decrypt", "-d", help="Decrypt the message using private key", action='store',
                        default=False, metavar=('PRIVATE_KEY_FILE', 'MESSAGE OR FILE'), dest="decrypt", nargs=2)
    args = cli_parser.parse_args()

    return args


# =============================================================================
def pw_create_rsa_key(pattern, bits=4096):

    """
    Create a pair of keys (private and public) based on RSA. The keys are saved to
    <pattern>.pem and <pattern>.pem.pub, respectively.

    https://en.wikipedia.org/wiki/RSA_(cryptosystem)
    https://pycryptodome.readthedocs.io/en/latest/src/examples.html

    Args:
        pattern (str):  Pattern to name the key files
        bits (int): Number of bits to create the RSA key

    """

    key = RSA.generate(bits)

    # Create private key file
    private_key = key.export_key()
    fileout = open(pattern+".pem", "wb")
    fileout.write(private_key)
    fileout.close()

    # Create public key file
    public_key = key.public_key().export_key()
    fileout = open(pattern+".pem.pub", "wb")
    fileout.write(public_key)
    fileout.close()


# =============================================================================
def pw_encrypt_msg(public_key_file, msg, fout_name="passwd_encrypted.bin"):

    """
    Encrypt a message (msg) with the public key (public_key_file)

    Args:
        public_key_file (str): Filename
        msg (str): Message to be encrypted
        fout_name (str): Filename of the encrypted message

    Returns:
        Return the encrypted string

    """

    fpublic = open(public_key_file, 'rb')
    publickey = RSA.importKey(fpublic.read())
    public_crypter = PKCS1_OAEP.new(publickey)
    enc_data = public_crypter.encrypt(msg.encode())
    f_out = open(fout_name, 'wb')
    f_out.write(enc_data)
    f_out.close()
    fpublic.close()

    return enc_data


# =============================================================================
def pw_decrypt_msg(private_key_file, cypher_data):

    """
    Decrypt a message (msg) with the public key (public_key_file)

    Args:
        private_key_file (str): Filename
        cypher_data (str or filename): String or file containing the message to be decrypted

    Returns:
        Return the decrypted string

    """
    wd = os.getcwd()
    # DECRYPT with private_key
    fprivate = open(private_key_file, 'rb')
    private_key = RSA.importKey(fprivate.read())
    fprivate.close()
    public_crypter = PKCS1_OAEP.new(private_key)

    try:
        if os.path.isfile(os.path.join(wd, cypher_data)):
            with open(cypher_data, 'rb') as fin:
                enc_data = fin.read()
                dec_data = public_crypter.decrypt(enc_data)
    except TypeError:
        dec_data = public_crypter.decrypt(cypher_data)

    return dec_data


# ==============================MAIN PROGRAM===========================================
if __name__ == '__main__':

    """
    Main program to be called from CLI
    """

    print("======== Crypto Password: Start Job ========")
    arg = pw_parse_arguments()

    if len(sys.argv) <= 1:
        pw_print_header()

    if arg.usage:
        pw_print_header()

    if arg.version:
        print('passwd_encrypt.py version: {} ({})'.format(VERSION, DATE))

    # Create keys
    if arg.createkeys:
        pw_create_rsa_key(arg.createkeys)
        print("Private file was created in {}".format(arg.createkeys+".pem"))
        print("Public  file was created in {}".format(arg.createkeys + ".pem.pub"))

    # Encrypt message
    if arg.encrypt:
        fout_name = "passwd_encrypted.bin"
        pw_encrypt_msg(arg.encrypt[0], arg.encrypt[1], fout_name=fout_name)
        print("Message encrypted in {}".format(fout_name))

    # Decrypt message
    if arg.decrypt:
        m = pw_decrypt_msg(arg.decrypt[0], arg.decrypt[1])
        print(m.decode())

    print("======== Crypto Password: Job Done =========")



