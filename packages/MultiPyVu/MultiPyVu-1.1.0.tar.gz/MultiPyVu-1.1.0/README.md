![qd_logo](https://qdusa.com/images/QD_logo.png)
# MultiPyVu
***
---
### Introduction
MultiPyVu provides the ability to control the temperature, magnetic field, and chamber status of Quantum Design, Inc. products using python.  This module includes MultiVuServer(), which runs on the same computer as MultiVu, and MultiVuClient(), which is used to send commands to the cryostat.  MultiVuClient() can run (1) locally on the same PC as MultiVu + MultiVuServer(), or (2) remotely on another computer that has TCP access to the computer running MultiVuServer().

MultiVuDataFile() is a class which allows a python script to save data in a MultiVu-readable *.dat* format. Any data can be saved using this class, so it is easy to combine temperature and field data along with the output from a researcher's own instrumention.

The components of MultiPyVu enable access to the set and read the temperature, field, and chamber on the following QD platforms: PPMS, DynaCool, VersaLab, MPMS3, and OptiCool. MultiVuClient() can run on a PC, Mac, or Linux, including a RaspberryPi.

### Module Requirements
Before downloading MultiPyVu, be sure to have the following modules installed:
- python version 3.6 or higher
- pywin32 - *We reccomend using version 300 or higher.*
- pandas

For the Python 3 distribution Quantum Design recommends Anaconda (https://www.anaconda.com/products/individual) as it includes most modules needed for this server and other packages useful for scientific computing.  This code was built and tested using Python 3.8.  If you are not sure which version of Python you are using, from a command prompt type:
```
python --version
```

It is necessary to have the pywin32 module with at least version 300 installed on the computer which is running the server, which can be installed using an Anaconda prompt and typing:
```
conda install -c conda-forge pywin32
```
*Note: the latest version of pywin32 is not on the ananconda channel, and one must use the conda-forge channel indicated above.*

### Included Example Scripts
Several examples have been uploaded to Quantum Design's Pharos database and can be downloaded here.  These examples demonstrate various capabilities of the module, and serve as templates upon which users can add their own code to integrate external hardware operations with the enviornemntal controls of the Quantum Design instrument.
| Filename | Description|
-----|-----
example_Local.py | A simple script which starts the server, then the client, on the PC running MultiVu.  It relays basic instrument parameters and status to demonstration communication, serving as a minimum working example useful for testing basic functionality.
example_Remote-Server.py | For remote operation; this script must be running on the on the control PC along with the MultiVu executable.
example_Remote-Client.py | For remote operation; this script runs on a separate PC and relays basic instrument parameters and status to demonstration communication.
example_Command-Demos.py | Utilizes most basic functions of the module, setting temperature/field/chamber operations, reading back the values and status of those parameters, and waiting for stability conditions to be met.  As-written, it runs in local mode.
example_MVDataFile-VISA.py | Basic example showing how to route environmental parameters and data from external intruemnts into a single MultiVu-readable *.dat* file.  As-written, it runs in local mode.

### Getting Started
Before starting the server, be sure that the MultiVu executable is running on the PC connected to the cryostat. For testing purposes, you can use MultiVu in simulation mode on an office computer, or you can run MultiVuServer.py in scaffolding mode in which the server will simulate MultiVu.  This can be helpful for testing scripts on a computer that does not have MultiVu.  To run the server in scaffolding mode with DynaCool, type:
```
python MultiVuServer.py -s 
```
**Local Operation**
It is suggested to run first run the 'Local' example with no changes on the MultiVu PC connected to the instrument- this should verify that the underlying resources required by the module are all present and functioning properly.  If this is successful, proceed to the 'Command-Demos' example for a brief demonstration of the commands used to set and monitor the sample space environmental parameters, as well as the wait command.

**Remote Operation**
After confirming the local example scripts have exectued correctly, remote operation can be attempted.  First, on the MultiVu PC, run the 'Remote-Server' script, being sure to update the IP address to reflect the IPV4 address of the server PC.  To determine this address on a Windows PC, open a command prompt, change the directory to the location of the downloaded example files, and run the following command:
```
whats_my_ip_address
```
This executes a small batch file of the same name which returns the IPV4 address needed to facilitate remote operation.  Update the existing address the 'flags' variable of the 'Remote-Server' script and then run it.

Similarly, on the client PC, update the 'host' variable of the 'Remote-Client' script *with the same server PC IPV4 address* and run it.  The script will report the present temperature and field value/status a few times to demonstrate the connection is functioning.

**Next Steps**
Once the operating mode (local or remote) has been successfully tested, the user is encouraged to run the Command-Demos example to see a series of short examples demonstrating how cryostat control operations work using the syntax of the module.

It may sometimes be desirable to combine the sample enviornemnt parameters (temperature, field) with readings from a user's own instrumentation into a single *.dat* file which can be plotted in MultiVu.  This functionality, accomplished using the MultiVuDataFile class, is demonstrated using PyVISA to communicate with a VISA-compatible instrument in the  'MVDataFile-VISA' example.  Note that for this routine to execute properly, the correct instrument bus/address and query string need to be updated in the script.

For further information on the detailed operation of the components of the module, see the following sections.

### Using MultiVuServer() and MultiVuClient()
To start the server on localhost, open MultiVu, and then, using the example script _run_server.py_, go to a command prompt and type:
```python
python run_server.py
```
Note that one can also run the server and client in one script.  See the example_server_and_client.py file for an example.

There are a list of useful flags to specify settings.  These can be found by typing -h, which brings up help information:
```python
python run_server.py -h
```

One can specify the PPMS platform, but if MultiVu is running, specifying the platform should not be necessary.  For example:
```python
python run_server.py opticool
```

The server IP address can be spcified using the -ip flag.  For example, to specify an IP address of 127.0.0.1
```python
python run_server.py -ip=127.0.0.1
```
This flag is necessary if the server and client are going to be running on two different computers.  If they are on the same computer, then the -ip flag can be omitted and server will use 'localhost.'  To determine the server computer's IP address, type ipconfig at a command shell prompt and look for the IPv4 address.

To write a script which connects to the server from a client machine, put all of the commands to control the cryostat inside a with block:
```python
from MultiPyVu import MultiVuClient as mvc

with mvc.MultiVuClient('127.0.0.1') as client:
    <put program here>
<do any post-processing once the client has been closed>
```

If needed, the host and port can be specified as parameters to MultiVuClient().

Alternatively, one can start a connection to the server using:
```python
client = mvc.MultiVuClient(host='127.0.0.1')
client.open()
<put program here>
client.close_client()
<do any post-processing once the client has been closed>
```

The client can also end the program by closing the server at the same time using
```python
client.close_server()
```

If the client and server are being run on the same computer, then one could also write one script to control them both.
```python
from MultiPyVu import MultiVuServer as mvs
from MultiPyVu import MultiVuClient as mvc

with mvs.MultiVuServer() as server:
    with mvc.MultiVuClient() as client:
        <put program here>
<do any post-processing once the client and server have been closed>
```

### Commands
The commands to set and get the temperature, field, and chamber status are defined here:

**Temperature**
```python
client.set_temperature(set_point,
                       rate_K_per_min,
                       client.temperature.approach_mode.<enum_option>)
```

Note that the mode is set using the client.temperature.approach_mode enum. The temperature and status are read back using:
```python
temperature, status = client.get_temperature()
```
The possible status values can be listed by typing
```python
state_code_dictionary = client.temperature.state_code_dict()
```

**Field**
```python
client.set_field(set_point,
                 rate_oe_per_sec,
                 client.field.approach_mode.<enum_option>)
```
Note that the approach mode is set using the client.field.approach_mode enum. The PPMS magnet can be run driven or persistent, so it has a fourth input
which is specified using the client.field.driven_mode enum.  For the PPMS flavor:
```python
client.set_field(set_point,
                rate_oe_per_sec,
                client.field.approach_mode.<enum_option>,
                client.field.driven_mode.<enum_option>)
```
The field and status are read back using:
```python
field, status = client.get_field()
```
and the possible status values can be found using the client.field.state_code_dict()

**Chamber**
```python
client.set_chamber(client.chamber.mode.<enum_option>)
```
And read back using:
```python
chmbr = client.get_chamber()
```
**Wait For**
When a setting on a cryostat is configured, it will take time to reach the new setpoint.  If desired, one can wait for the setting to become stable using the .wait_for(delay, timeout, bitmask) command.  A delay will set the time in seconds after the setting is stable; timeout is the seconds until the command will give up; bitmask tells the system which settings need to be stable.  This can be set using the client.subsystem enum.  Multiple settings can be configured using bitwise or.  For example:
```python
client.wait_for(0, 90, client.subsystem.temperature | client.subsystem.field)
```

### Saving to a MultiVu Data File
The MultiVuClient class can be used in conjunction with 3rd party tools in order to expand the capabilities of measurements from a Quantum Desing cryostat. One can set up a VISA connection to a voltmeter, for example, and then collect information while controlling the cryostat temperature, field, and chamber status.  This data can be collected into a MultiVu data file using MultiVuDataFile.py.  First, import this into a script, then instantiate the MultiVuDataFile() class.  Then assign the column headers and create the file:
```python
from MultiPyVu import MultiVuDataFile

# configure the MultiVu columns
data = MultiVuDataFile()
data.add_multiple_columns(['Temperature', 'Field', 'Chamber Status'])
data.create_file_and_write_header('myMultiVuFile.dat', 'Special Data')
```
Data is loaded into the file using .set_value(column_name, value), and then a line of data is written to the file using .write_data() For example:
```python
temperature, status = client.get_temperature()
data.set_value('Temperature', temperature)
data.write_data()
```
### Testing the Server Using Scaffolding
For testing the server, QD has supplied scaffolding for the MultiVu commands to simulate their interactions with the server. This can be helpful for writing scripts on a computer which is not running MultiVu. To use this, start the server in scaffolding mode by using the -s flag:
```python
python run_mv_server.py PPMS -s
```
### Troubleshooting
Typical connection issues are due to:
- Firewall. You might need to allow connections on port 5000 (the default port number) in your firewall.
- Port conflict. If port 5000 is in use, a different number can be specified when instantiating MultiVuServer() and MultiVuClient().
```python
server = mvs.MultiVuServer(port=6000)
client = mvc.MultiVuServer(port=6000)
```
- A log file named QdMultiVu.log shows the traffic between the server and client which can also be useful during troubleshooting.

## Contact
Please reach out to apps@qdusa.com with questions or concerns concerning MultiPyVu.

![qd_logo](https://qdusa.com/images/QD_logo.png)
