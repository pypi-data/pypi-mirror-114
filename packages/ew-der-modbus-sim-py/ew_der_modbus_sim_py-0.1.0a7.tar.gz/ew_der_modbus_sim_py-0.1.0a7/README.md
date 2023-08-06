<div align="center">
  <a href="https://www.energyweb.org/"><img src="https://www.energyweb.org/wp-content/uploads/2019/04/logo-brand.png" alt="EnergyWeb" width="150"></a>
  <h1 style="padding:25px;">
    EnergyWeb DER Modbus Simulator
  </h1>
</div>


## Introduction
This repository hosts the EnergyWeb's Decentralized-Energy-Resouce Modbus Simulator.

## Primary features
- TCP/RTU modbus support.
- Sunspec interface support.
- Supply custom DER model.
- Model-map library available.

## Prerequisites
- ```pip>=20.3.4```
- ```pipenv>=2020.8.13```

## Quick start

### Installation steps
```
# Clone demo repository
git clone https://github.com/energywebfoundation/ew_der_modbus_sim_py.git

# Acces project folder
cd ew_der_modbus_sim_py

# Installs pipenv
pip install pipenv --upgrade

# Creates a python3 virtual environment
pipenv --three

# Installs all demo dependencies
pipenv install '.[all]'
```

### Preset environment variables
```
# Modbus Mode [TCP or RTU]
SLAVE_MODE=TCP
# A slave unique ID [int]
SLAVE_ID=1

# Slave TCP address and port. Defaults to 'localhost:8502'
SLAVE_TCP_ADDRESS=localhost
SLAVE_TCP_PORT=8502

# Slave RTU port 
SLAVE_RTU_PORT=/dev/ptyp5

# DER model-map name 
MODEL_MAP_NAME=STP8-10-3AV-40
```

### Virtual environment
```
# Access pipenv's virtual environment in order to run the examples below
pipenv shell
```

## Documentation
### DER Simulator

```
# Running Simulator
python3 ./src/ew_der_modbus_sim_py/der_simulator.py
```

### Available model-map list
- SMA
  - STP8-10-3AV-40 - PV Inverter
  - SUNNY-ISLAND-4.4-M-13 - Battery Inverter 

## Active Contributors
- Ioannis Vlachos (@iovlachos)
- Mahir Şentürk (@mhrsntrk)
- Bacem Ben Achour (@Aresguerre) 
- Pablo Buitrago (@ChangoBuitrago)

License
-------
This project is licensed under GNU General Public License Version 3 (GPLv3)