# Documentation – Safety and Security

## RSA Algorithm

This project involves the implementation of the RSA algorithm for secure communication. The RSA algorithm provides a method for secure data transmission by utilizing public and private keys. If you're new to the RSA algorithm, you can refer to this helpful article: [How Does RSA Work](https://hackernoon.com/how-does-rsa-work-f44918df914b).

## Visual Presentation
![image](https://github.com/PavelSilviu/ISSA-SAFETY-SECURITY/assets/45463347/4ee70d53-b713-4cd6-bf01-5ac27bb5eac6)
![image](https://github.com/PavelSilviu/ISSA-SAFETY-SECURITY/assets/45463347/ead2cdd0-e8e1-401a-b268-cfe21fdce609)


**Important Considerations:**
- The algorithm deals with hex numbers, so make sure to pass hex numbers converted into integers as arguments for the decryption and encryption functions.
- The private key is generated using the multiplicative inverse algorithm. For more details, you can refer to this [Multiplicative Inverse Algorithm](http://www-math.ucdenver.edu/~wcherowi/courses/m5410/exeucalg.html) explanation.

## TCP Sockets

In this project, TCP sockets are used to establish communication between clients and servers. TCP (Transmission Control Protocol) is chosen for its reliability and in-order data delivery characteristics.

**Why Use TCP:**
- It ensures reliability by detecting and retransmitting dropped packets.
- It delivers data in the order it was sent, which ensures in-order data delivery.

For more information on TCP sockets and their usage in Python, check out this [Real Python article](https://realpython.com/python-sockets).

## Graphical Interfaces

### Server Interface

The server interface is designed to start the server and wait for client connections. Once a client is connected, a message will be displayed under the button. The "key" button is initially disabled until a client connection is established. Upon pressing the key button, "the car is unlocked," and the dashboard is displayed on the screen.

The dashboard serves as a warning zone where specific errors are displayed. These errors include:
- **Airbag On:** This error appears when the client sends a hex number with the format LOW = 0x01 and HIGH = ~LOW.
- **Low Corruption (LC)/High Corruption (HC):** These errors appear when the client sends hex numbers that do not match the specified formats.

### Client Interface

The client interface begins with disabled buttons, which are enabled after pressing the key button on the server interface. The client can establish a connection with the server and receive a response text. The client can send messages in different formats:
- LOW = 0x01 and HIGH = ~LOW: The server executes the command, and a response message is displayed.
- LOW = 0x57: The server executes the command, and a response message is displayed.
- HIGH != ~LOW: The server executes the command, and a response message is displayed.

## How the Program Works - Airbag ON Simulation

The program involves a server-client interaction. The server "unlocks" the car, and the client begins sending hex numbers to the server. The airbag simulation activates when the hex number format matches:
- LOW = 0x01
- HIGH = ~LOW

When the "key" button is pressed on the client interface, a hex number (0xfe01) is encrypted using the RSA algorithm and sent to the server. The server decrypts the number, checks conditions, and starts the airbag if requirements are met.

In cases where the number format does not match, two possible warnings appear:
- LOW != 0x01 – Low Corruption
- HIGH != ~LOW – High Corruption

Pressing the "key" button again will disable the client interface.

## References

- [RSA Algorithm Explanation](https://hackernoon.com/how-does-rsa-work-f44918df914b)
- [Multiplicative Inverse Algorithm](http://www-math.ucdenver.edu/~wcherowi/courses/m5410/exeucalg.html)
- [TCP Socket Diagram](https://commons.wikimedia.org/wiki/File:InternetSocketBasicDiagram_zhtw.png)
- [Python Sockets](https://realpython.com/python-sockets)
