# tor-master.py

This Python script is used to manage multiple identities in the Tor network. It provides a simple menu-driven interface to create, start, and restart Tor identities. Each identity is a separate instance of the Tor browser, running on its own SocksPort and ControlPort.

## Requirements

- Python 3.6 or higher
- `termcolor` Python library

## Installation

1. Install Python 3.6 or higher if you haven't already. You can download it from the official Python website: https://www.python.org/downloads/

2. Install the `termcolor` library using pip:

```bash
pip install termcolor
```

3. Download the Tor Browser Bundle from the official Tor Project website: https://www.torproject.org/download/

4. Extract the downloaded file to a directory named `tor-browser` in the same directory as the `tor-master.py` script.

## Usage

Run the script using Python:

```bash
python tor-master.py
```

This will start the script and display a menu with the following options:

1. Create an additional identity
2. Start an identity
3. Restart all identities
4. Exit

### Create an additional identity

This option will create a new Tor identity. It does this by copying the `tor-browser` directory to a new directory named `TOR-IDENTITY_n`, where `n` is the number of the new identity. It then creates a `user.js` file in the new identity's profile directory with the necessary preferences set for the new SocksPort and ControlPort.

### Start an identity

This option will start a Tor identity that is not currently running. It does this by running the `start-tor-browser` script in the identity's directory.

### Restart all identities

This option will stop all running Tor identities and delete their directories, effectively resetting all identities.

### Exit

This option will exit the script.

## Note

This script should not be used for any illegal activities. The author is not responsible for any misuse of this script. And of course, it is strictly prohibited to use it in any private and/or commercial company.