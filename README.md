# Socket Based TicTacToe

## Overview

This Python project implements a TicTacToe game using socket communication. It consists of two main files: `ServerClient.py` and `Client.py`. The `ServerClient.py` file hosts the TicTacToe game and acts as the server, allowing players to connect and play as the host. On the other hand, the `Client.py` file connects to the host server to play the game as a client.

## Requirements

All requirements should already be installed on your device when Python is installed, but if for some reason they are missing this are the ones i use:

`pip install threading`
`pip install socket`


## Usage

To play the TicTacToe game:

1. Run `ServerClient.py` to host the game.
2. Before running `Client.py`, make sure to edit the file and replace "IP-ADDRESS-HERE" in the `connectToGame()` function with the host's local IP address. (The Local-IP Address will be displayed inside of the `ServerClient.py`'s Terminal)
3. Run `Client.py` to connect to the hosted game and play as a client.

## Features

- Socket-based communication for multiplayer functionality.
- Support for hosting and joining games.
- Clear console interface for displaying the TicTacToe board.
- Error handling for invalid inputs and game termination.

## Future Improvements

- Add `Server.py` for standalone host.
- Add support for multiple concurrent games on the server.
- Improve error handling and input validation.
