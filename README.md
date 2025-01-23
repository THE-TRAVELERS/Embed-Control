# Embed-Control

> This repository contains the source code for the embed part of the project.

![Schema](/assets/schema.jpg)

## Control - python

The control part of the project is responsible for getting the decisions of the user and the manual controller (movement inputs).

Today, it is a simple script, but it will be improved in the future to first become a TUI (and stay that way for manual debug). Then, the feature and endpoints will be implemented to the control panel of the project (Flutter project).

## Command

### ESP - C++

The ESP is a command board for the motors (land and water propulsion) that will translate the controller inputs into the correct signals for the motors drivers.

Other features are to expect such as relays control, leds and more.

### Rpi - python

The embedded Raspberry Pi will be responsible for the communication between the ESP and the control panel (Flutter project). It gathers and transmit user inputs to the ESP and send sensors data to the control panel (user).

It is an API with two main features: get the status of the websockets (open/close) and access the websockets to receive/send data.

## Installation

### Rpi

#### Using Docker

Docker is a tool designed to make it easier to create, deploy, and run applications by using containers. Containers allow a developer to package up an application with all parts it needs, such as libraries and other dependencies, and ship it all out as one package.

On the Raspberry Pi, the installation is a little bit different from the common OS. The official documentation is **[here](https://docs.docker.com/engine/install/debian/)**.

The all-in-one command to install Docker on the Raspberry Pi is:

```bash
curl -fsSL https://get.docker.com | sh
```

TODO: change to clean install.

Once set up, clone the repository:

```bash
git clone https://github.com/THE-TRAVELERS/Embed-Control.git
```

Move to the directory:

```bash
cd Embed-Control/src/command/Rpi
```

Run the docker build command:

```bash
docker compose build
```

And then, run the up command:

```bash
docker compose up -d
```

The service will be up and running. To check the logs, we may use the tool `lazydocker`:

```bash
curl https://raw.githubusercontent.com/jesseduffield/lazydocker/master/scripts/install_update_linux.sh | bash
```

Now you should be able to access the logs of your containers using:

```bash
lazydocker
```

#### Manually

First clone the repository and navigate to `Embed-Control/src/command/Rpi` (steps above).

Then, let's set up a virtual environment:

```bash
python3 -m venv travenv
source travenv/bin/activate
```

Then, install the requirements:

```bash
pip install -r requirements.txt
```

Now, we can run the FastAPI server for a debug environment:

```bash
fastapi dev /app/main.py --port 8000
```

Or for a production environment:

```bash
fastapi run /app/main.py --port 8000
```

### ESP

> [!NOTE]
> WIP

### Client

> [!NOTE]
> WIP

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
