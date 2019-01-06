# Korad PSU  serial protocol
Korad `K[A|D][30|60][05|10]P` series PSUs provide a programmable interface to control the PSU over a virtual serial port over USB or via an RS232 interface. 

## Virtual Serial Port Parameters:

|parameter        | value |
|----------------:|:-----:|
|Baud Rate        | `9600`|
|Parity bit       | `None`|
|Data bit         | `8`   |
|Stop bit         | `1`   |
|Data flow control| `None`|

## Protocol and Commands:

### Format
All commands are in plain-text and follow the basic format :

```
<CMD><X>:<Y>
```
**_OR_**
```
<CMD><X>?
```

Where:

| Part |Description |
|-----:|:-----------|
|`CMD` | command    |
| `X`  | parameter 1|
| `Y`  | parameter 2|

*`NOTE:`* For single channel units, use `1` as the output channel.

Response time for set commands is approximately 50ms.

### Command Listing:

#### `ISET<X>:<Y>`
Description: Sets the output current.

Example: `ISET1:2.225`
Sets the CH1 output current to 2.225A.

#### `ISET<X>?`
Description: Returns the output current setting.

Example: `ISET1?`
Returns the CH1 output current setting.

#### `VSET<X>:<Y>`
Description: Sets the output voltage.
Example: `VSET1:20.50`

Sets the CH1 voltage to 20.50V

#### `VSET<X>?`
Description: Returns the output voltage setting.

Example: VSET1?
Returns the CH1 voltage setting

#### `IOUT<X>?`
Description: Returns the actual output current.

Example: IOUT1?
Returns the CH1 output current

#### `VOUT<X>?`
Description: Returns the actual output voltage.

Example: VOUT1?
Returns the CH1 output voltage.

#### `OUT<X>`
Description: Sets the output according to provided Boolean `X` where `X` can hold values:

|Boolean Value| Syntax|
|-:|:-|
|True |`1`|
|False |`0`|

Example: `OUT1`
Turns on the output.

#### `STATUS?`
Description: Returns the Power supply status.
Contents 8 bits in the following format

|Bit                |Item       |Description    |
|------------------:|:----------|---------------|
|`0`                |CH1 status | `0=CC`, `1=CV`|
|`1`,`2`,`3`,`4`    |   N/A
|`5`                |OCP status |`0=OFF`, `1=ON`| 
|`6`                |Output     |`0=OFF`, `1=ON`|
|`7`                |   N/A                     |    

#### `*IDN?`
Description: Returns the unit identification.

Example: `*IDN?` will return 
```
KORAD KD3005P V2.0 (Manufacturer, model name,)
```

#### `RCL<X>`
Description: Recalls a panel setting from memory location `X`, where `X` is memory number `1` to `5`.

Example: `RCL1`  Recalls the panel setting stored in memory number `1`.

#### `SAV<X>`
Description: Stores the **current** panel setting to memory location `X`, where `X` is memory number `1` to `5`.

Example: `SAV1`
Stores the **current** panel setting in memory number 1

#### `OCP<X>`
Description: Set over current protection enable status according to provided Boolean `X` where `X` can hold values:

|Boolean Value| Syntax|
|-:|:-|
|True |`1`|
|False |`0`|

Example: `OCP1`
Toggles OCP for channel 1.
