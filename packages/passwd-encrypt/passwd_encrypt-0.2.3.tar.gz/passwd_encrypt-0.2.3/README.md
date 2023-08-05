# Example Package as library

This is a simple package to encrypt and decrypt strings using RSA keys.

A possible application can be to encrypt a password when [parakamiko library](http://www.paramiko.org/) is used to make a SSH connection with password. Although is preferable to make a key without password to the SSH connection, sometimes this method does not work, for example if you need to make a connection to **localhost**

As example:

This code is not recommend due to the password is going in plain text
```python
import paramiko
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname='localhost', username='user', password='12345678')
client.exec_command('ls', timeout=5)
```

This code is better:

*  First generate the encrypted password in a file.:

```python
from passwd_encrypt.passwd_encrypt import pw_create_rsa_key, pw_encrypt_msg
# First you generate a couple of RSA keys and then encrypt the password.
pw_create_rsa_key("mykey")
public_key="mykey.pem.pub"
pw_encrypt_msg(public_key, '12345678')
# The password is stored in a cyphered file named "passwd_encrypted.bin"
```

* Now in the code using paramiko to stablish a SSH connection, use the following commands:

```python
import paramiko
from passwd_encrypt.passwd_encrypt import pw_decrypt_msg

# Get the pass_decrypt
private_key="mykey.pem"
pass_decrypt = pw_decrypt_msg(private_key, "passwd_encrypted.bin")

# SSH connection
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname='localhost', username='user', password=pass_decrypt)
client.exec_command('ls', timeout=5)
```
The important here is to get the generated private_key in a safe place.
Using this library you can distibute a source code with SSH connection based on passwords without to reveal the password in the code.

# Example Package as program from the CLI

The program can also be use from the CLI (command line interface) as follows:

1. Activate the python enviroment (if needed)
2. Get the usage or help from the program

```python
python passwd_encrypt.py -u


======== Crypto Password: Start Job ========

#############################################
#            PASSWD_ENCRYPT                 #
#           Dr. Javier Ramos                #
#    Macromolecular Physics Department      #
#              IEM-CSIC                     #
#       https://github.com/jrdcasa          #
#############################################
 Usage:
 passwd_encrypt [--createkeys|-c] <pattern>  # Generate the private and public keys as <pattern>.pem and <pattern>.pem.pub, respectively in the working directory.
 passwd_encrypt [--encrypt|-e] <rsa public key file> <message to encrypt>   # Encrypt message with the public key.
 passwd_encrypt [--decrypt|-d] <rsa private key file> <string or file containing the message to decrypt>  # Decrypt message with the public key.

======== Crypto Password: Job Done =========
```


A example is available in the **recipes** folder as jupyter notebook.
