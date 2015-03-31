pysmartenv
==========

This project provides a Control Interface (CI) module for an assistive domotics system called SMAD.
The CI is responsible of receiving commands by an RPC server and communicating with the Arduino plate, which will operate the desired device.
Also, CI module offers a GUI for the end-user.

The SMAD project is a research project from Universidade Federal do Espirito Santo (UFES), presented in:
+ [Flavio Ferrara's M.Sc. thesis]()
+ [Video](https://vimeo.com/122515785)
+ ...more coming

This CI needs to be coupled to a Biological Signal Transducer (BST) in order to the entire system to be employed. Two examples of BSTs are provided in this twin [project](https://github.com/ienaplissken/pyassistive).

Dependencies
------------
+ Python 2.7 (complete installation with Tk library)
+ pyserial (Arduino communication)
+ [jsonrcptcp](https://github.com/joshmarshall/jsonrpctcp/tree/master/jsonrpctcp), a JSON-RPC library (Apache 2.0 license)

Menu panel
-----------
Template of a JSON Panel descriptor file.

```json
{
  "panels": [{
      "id" : 1,
      "items" : [
        {  "name" : "Device 1 name",
           "imgOff" : "Path of image OFF",
           "imgOn" : "Path of image OFF",
           "deviceOperation": "switch",
           "message" : "dv1"
       },
       {  "name" : "Device 2 name",
           "imgOff" : "Path of image OFF",
           "imgOn" : "Path of image OFF",
           "deviceOperation": "device_on",
           "message" : "dv2"
       }
      ]
    },{
    "id" : 2,
    "items" : []
  }]
}
```

When an option concerns the operation of a device, it needs to specify the kind of operation.
This is done with the attribute "deviceOperation".
  - deviceOperation = "switch" inverts the current state
  - deviceOperation = "device_on" turns on the device if it's off
  - deviceOperation = "device_off" turns off the device if it's on
  - deviceOperation = "device_modify" changes a property of the device
When an option with deviceOperation = "device_modify" is triggered, the interface will show the ON icon for 1 second. For the other kind of operation, the ON icon will be shown until the
next option trigger.
