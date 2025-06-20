# napass

### Installation
1. Make sure Python3 (>=3.13) is installed
2. `pip3 install requirements.txt`
3. Execute `./napass` shell script

### Quick start

Initiate a new vault by running the following command:

```
./napass init
```

Specify the *name* of your Vault and the *password*. For now, or maybe forever, there's no way to restore vault
password, so please remember it.

You'll be dropped into NAPASS shell session.
Now go experiment through using some commands. You can get a list by typing `help`. You'll get there :)

### Some details

Vaults are stored in encrypted files, which contain sensitive user data. The structure looks something like this:

```
+------------------------------------------------------------------------+
| [salt] <=> base64( encrypted(data) ) <=> base64( encrypted(metadata) ) |
+------------------------------------------------------------------------+
```

Napass prepends the encrypted vault file with 16 byte salt (using *PBKDF2HMAC* cryptographic function). The last
part is constructed of encoded and encrypted (by Fernet) toml data, null-byte separator, and special metadata which NAPASS uses to differentiate between hidden and non-hidden fields. 

