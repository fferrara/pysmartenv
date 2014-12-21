pysmartenv
==========

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
