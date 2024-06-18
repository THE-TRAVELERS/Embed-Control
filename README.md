# Embed-Control

> This repository contains the source code for the embed part of the project.

## Control - python

The control part of the project is responsible for getting the decisions of the user and the manual controller (movement inputs).

Today, it is a simple script, but it will be improved in the future to first become a TUI (and stay that way for manual debug). Then, the feature and endpoints will be implemented to the control panel of the project (Flutter project).

## Command

### ESP - C++

The ESP is a command board for the motors (land and water propulsion) that will translate the controller inputs into the correct signals for the motors drivers.

Other features are to expect such as relays control, leds and more.

### Rpi - python

The embedded Raspberry Pi will be responsible for the communication between the ESP and the control panel (Flutter project). It gathers and transmit user inputs to the ESP and send sensors data to the control panel (user).

It is supposed to become an API hosted using Docker for stability, scalability and reliability.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
