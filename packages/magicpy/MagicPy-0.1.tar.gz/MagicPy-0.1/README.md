# MagicPy

This toolbox can be used to communicate with MagVenture TMS stimulators via python.  
For the most part it's just a python translation of the Magventure part of the MAGIC toolbox (https://github.com/nigelrogasch/MAGIC). If you use this toolbox, please also cite the original MAGIC toolbox.

This is no official tool, for use at own risk.

## Installation
Just clone this repository and install:

``` bash
git clone https://gitlab.gwdg.de/tms-localization/utils/magicpy
cd magicpy
python setup.py

```
It has been tested with python<=3.6 on Windows and Linux, I guess it should also work with MacOS - feel free to drop me a line if this is the case.

## Usage
- Connect the stimulator control port to a serial port of your computer. 
- Find out which port it is:

``` python
import magicpy as mp
mp.list_ports()
> /dev/ttyS0: ttyS0 [PNP0501]

```

- Initialize `MagVenture()` object and connect:

``` python
stimulator = mp.MagVenture('/dev/ttyS0')     # Initialize the stimulator object
stimulator.connect()                         # This opens the serial connection
```

Now you're ready to go:

``` python
# send single, biphasic pulse with reversed current direction, 50%MSI:
stimulator.arm()                                   # Enable stimulator
stimulator.set_amplitude(50)                       # Set stimulation intensity to 50% MSO

# Setting pulse settings like this takes a few setting:
stimulator.set_current_dir('Reversed')  
stimulator.set_waveform('Biphasic')

# To speed this up, provide all settings at once:
stimulator.set_waveform(waveform='Biphasic', current_dir='Reversed', n_pulses_per_burst=2, ipi=1, baratio=1)

resp, error = stimulator.fire(get_response=True)   # Send TMS pulse and get stimulator response

stimulator.disarm()                                # Disable
stimulator.disconnect()                            # Free port access when you're done

print(resp)                                        # You can use the stimulator response to the TMS pulse to log youre experiment
print(stimulator.get_status())                     # Some more stimulator settings 
```

## Caveats
- Using the serial connection to control the stimulator does not deactivate the stimulators menu. It's possible (and perfectly fine) to change parameters at the stimulator after setting them with this toolbox. Per se, the toolbox is not notified about changes made at the stimulator itself. This means you should not rely your data analysis on the settings you sent to the stimulator, but rather use the logfiles of the actual stimulations.  
- You can send TMS pulses with the `fire()` method if you don't mind the high lag and jitter. If timing is important always send trigger pulses via TTL to the TriggerIn port (jitter = 12µs) instead.
- When playing around with this toolbox make sure the TMS coil is not placed on any electronic devices...

## Troubleshooting
### No communication with stimulator
- Check connection. The stimulator might have two serial ports, try the other. You're computer might have several ports, did you specifiy the correct one?
- USB2serial adapters might cause problems. They need to provide the correct baudrate (=38400), not all are cabable of it.
- `stimulator.port.read()` should give you something after pressing buttons on the stimulator menu. If this is not the case, it's most probably a hardware related issue.


### Occasional problems fetching information from the stimulator
- Increase the waittime after sending a command to the stimulator before reading the response. Use the `wait_s` and `wait_l` parameters while initializing the stimulator object:
``` python
stimulator = mp.MagVenture('/dev/ttyS0', wait_s=3, wait_l=8)  # Set waittime to 3 seconds and 8 seconds
```

### Stimulator stops responding to commands sent via serial until restart
- This seems to happen if malformed commands are sent to the stimulator. This might be a bug in this toolbox or due to newer stimulator fimware versions. Feel free to open an issue about it.
