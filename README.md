A word about this repository:

This is my second attempt to create code with the use of AI. Only these few sentences at the top of the README are handwritten. 

I used ChatGPT on my Android mobile to start the project description and the specifications. This led to the first version of the README in Markdown. 

When the README was in a ready state, i proceeded with the Gemini extension inside VSCode. Gemini did all the coding according to the specifications in the README. Gemini introduced some minor suggestions for improvements. After finishing the code, the README was updated to match the code.

All this was done in one day, maybe 5-7 hours. The application seems to work fine and has a Mock/Test mode. There is no automated test environment.

**From here on: AI generated content.**

# Python USB UART Register Controller — Complete Project Specification

## 1. Project Overview

This project is a desktop application written in Python for controlling a USB UART hardware device through a graphical user interface (GUI).

The application communicates with the hardware through a one-way UART serial interface over USB. The hardware device only receives commands and does not transmit any response back to the application.

The application is register-oriented:

* every hardware register is represented directly in the GUI,
* the user can inspect the current cached register value,
* the user can enter a new hexadecimal byte value,
* and the user can transmit the value to the hardware device.

The application is designed using a layered architecture with clear separation between:

* GUI logic,
* application logic,
* and serial communication logic.

---

# 2. Technology Stack

| Component                    | Technology        |
| ---------------------------- | ----------------- |
| Programming Language         | Python            |
| GUI Framework                | PyQt 6.7 or newer |
| Serial Communication Library | pySerial          |
| Communication Type           | USB UART          |
| Target Platform              | Linux             |

---

# 3. UART Communication Specification

The UART communication uses the following fixed configuration:

| Parameter    | Value            |
| ------------ | ---------------- |
| Serial Port  | `/dev/ttyUSB0`   |
| Baud Rate    | 115200           |
| Data Bits    | 8                |
| Parity       | None             |
| Stop Bits    | 1                |
| Flow Control | None             |
| Direction    | PC → Device only |

The UART configuration is hardcoded and managed internally through a Python configuration class.

The configuration is not editable through the GUI.

---

# 4. Serial Packet Protocol

Each write operation transmits exactly 3 raw bytes:

```text
[0x77][REGISTER][DATA]
```

Where:

* `0x77` is a fixed synchronization/header byte,
* `REGISTER` is the one-byte register address,
* `DATA` is the one-byte register value.

Example:

```text
write(0x04, 0x21)
↓
Transmitted bytes:
0x77 0x04 0x21
```

All registers are handled independently as single-byte writes.

No:

* multi-register packets,
* grouped transactions,
* delays,
* acknowledgements,
* or receive handling

are required.

---

# 5. Application Architecture

The application uses the following layered architecture:

```text
GUI
    ↓
Application Controller
    ↓
Serial Service
    ↓
pySerial
    ↓
USB UART Device
```

---

## 5.1 GUI Layer

The GUI layer is responsible for:

* displaying register widgets,
* collecting user input,
* validating hexadecimal input,
* displaying cached register values,
* emitting write requests.

The GUI layer does not:

* communicate directly with pySerial,
* construct packets,
* manage UART configuration,
* or contain hardware logic.

---

## 5.2 Application Controller

The application controller is responsible for:

* application state management,
* register cache management,
* routing GUI events,
* synchronizing GUI state,
* invoking the serial service.

The controller translates GUI actions into register write operations.

---

## 5.3 Serial Service

The serial service is responsible for:

* pySerial integration,
* serial port opening,
* packet construction,
* serial transmission,
* **Mock mode simulation for hardware-less development.**

The serial service implements an **Abstract Base Class (ABC)** interface and exposes exactly one public function:

```text
write(register, data)
```

Where:

* `register` is a one-byte register address,
* `data` is a one-byte register value.

The serial service does not contain:

* GUI logic,
* application logic,
* or register semantics.

---

# 6. Connection Lifecycle

## 6.1 Application Startup

At startup:

```text
1. Initialize all register cache values to 0x00
2. Open serial port: /dev/ttyUSB0
3. Transmit all register values to hardware
4. Enable GUI interaction
```

The initial hardware state after startup is therefore all zero.

After initialization:

* register writes occur only after explicit user interaction.

---

## 6.2 Startup Failure Handling

If `/dev/ttyUSB0`:

* does not exist,
* or cannot be opened,

then:

1. a popup dialog is shown,
2. the user acknowledges the popup,
3. the application terminates immediately.

---

## 6.3 Runtime Transmission Failure Handling

If serial transmission fails during runtime:

1. a popup dialog is shown,
2. the user must close and restart the application.

There is:

* no reconnect functionality,
* no retry logic,
* no runtime recovery handling.

---

# 7. Threading Model

Serial communication occurs directly in the GUI thread.

No:

* worker threads,
* transmission queues,
* asynchronous communication,
* or timing schedulers

are required.

This is acceptable because:

* packets are very small,
* communication is transmit-only,
* no delays are required,
* no receive handling exists.

---

# 8. Configuration System

The application uses a Python configuration class.

The configuration contains:

* serial port definition,
* UART configuration constants,
* GUI constants.

The configuration is not editable through the GUI.

---

# 9. Project Folder Structure

The project structure is defined as:

```text
src/
    gui/
    controller/
    serial/
    config/
    models/
```

Folder responsibilities:

| Folder        | Responsibility                          |
| ------------- | --------------------------------------- |
| `gui/`        | PyQt GUI code                           |
| `controller/` | Application controller logic            |
| `serial/`     | Serial service and pySerial integration |
| `config/`     | Configuration definitions               |
| `models/`     | Dataclasses and shared models           |

---

# 10. Register Definition Data Model

The register definition model uses a Python dataclass.

The same dataclass type is used for all registers.

The dataclass conceptually contains:

| Field       | Purpose                    |
| ----------- | -------------------------- |
| Name        | Register display name      |
| Address     | Register address           |
| Description | Human-readable description |
| Group       | GUI grouping               |

The register system is data-driven and reusable.

---

# 11. Register List

| Reg # | Hex Addr | Name    | Description                      |
| ----- | -------- | ------- | -------------------------------- |
| 0     | 0x00     | FREQLO1 | Voice 1 frequency low byte       |
| 1     | 0x01     | FREQHI1 | Voice 1 frequency high byte      |
| 2     | 0x02     | PWLO1   | Voice 1 pulse width low byte     |
| 3     | 0x03     | PWHI1   | Voice 1 pulse width high nibble  |
| 4     | 0x04     | CTRL1   | Voice 1 waveform and control     |
| 5     | 0x05     | AD1     | Voice 1 ADSR attack and decay    |
| 6     | 0x06     | SR1     | Voice 1 ADSR sustain and release |
| 7     | 0x07     | FREQLO2 | Voice 2 frequency low byte       |
| 8     | 0x08     | FREQHI2 | Voice 2 frequency high byte      |
| 9     | 0x09     | PWLO2   | Voice 2 pulse width low byte     |
| 10    | 0x0A     | PWHI2   | Voice 2 pulse width high nibble  |
| 11    | 0x0B     | CTRL2   | Voice 2 waveform and control     |
| 12    | 0x0C     | AD2     | Voice 2 ADSR attack and decay    |
| 13    | 0x0D     | SR2     | Voice 2 ADSR sustain and release |
| 14    | 0x0E     | FREQLO3 | Voice 3 frequency low byte       |
| 15    | 0x0F     | FREQHI3 | Voice 3 frequency high byte      |
| 16    | 0x10     | PWLO3   | Voice 3 pulse width low byte     |
| 17    | 0x11     | PWHI3   | Voice 3 pulse width high nibble  |
| 18    | 0x12     | CTRL3   | Voice 3 waveform and control     |
| 19    | 0x13     | AD3     | Voice 3 ADSR attack and decay    |
| 20    | 0x14     | SR3     | Voice 3 ADSR sustain and release |
| 21    | 0x15     | FCLO    | Filter cutoff low bits           |
| 22    | 0x16     | FCHI    | Filter cutoff high bits          |
| 23    | 0x17     | RESFILT | Filter resonance and routing     |
| 24    | 0x18     | MODEVOL | Filter mode and master volume    |

---

# 12. GUI Design

## 12.1 General GUI Characteristics

The GUI is:

* register-oriented,
* engineering-focused,
* dark themed,
* vertically scrollable.

The GUI uses reusable register widgets grouped into logical hardware sections.

---

## 12.2 Main Window Layout

The main window:

* has a default size of `1400 x 1000`,
* uses vertical scrolling for the entire window,
* contains vertically stacked framed register sections.

---

## 12.3 Register Groups

The main window contains four framed vertical sections:

```text
Voice 1
Voice 2
Voice 3
Filter / Master
```

---

# 13. Register Grouping

## 13.1 Voice 1

| Addr | Register |
| ---- | -------- |
| 0x00 | FREQLO1  |
| 0x01 | FREQHI1  |
| 0x02 | PWLO1    |
| 0x03 | PWHI1    |
| 0x04 | CTRL1    |
| 0x05 | AD1      |
| 0x06 | SR1      |

---

## 13.2 Voice 2

| Addr | Register |
| ---- | -------- |
| 0x07 | FREQLO2  |
| 0x08 | FREQHI2  |
| 0x09 | PWLO2    |
| 0x0A | PWHI2    |
| 0x0B | CTRL2    |
| 0x0C | AD2      |
| 0x0D | SR2      |

---

## 13.3 Voice 3

| Addr | Register |
| ---- | -------- |
| 0x0E | FREQLO3  |
| 0x0F | FREQHI3  |
| 0x10 | PWLO3    |
| 0x11 | PWHI3    |
| 0x12 | CTRL3    |
| 0x13 | AD3      |
| 0x14 | SR3      |

---

## 13.4 Filter / Master

| Addr | Register |
| ---- | -------- |
| 0x15 | FCLO     |
| 0x16 | FCHI     |
| 0x17 | RESFILT  |
| 0x18 | MODEVOL  |

---

# 14. Register Widget Design

Each register is represented by a reusable register widget.

Each widget contains the following columns:

| Column        | Purpose                    |
| ------------- | -------------------------- |
| Register Name | Fixed label                |
| Address       | Register address           |
| Current Value | Cached current value       |
| New Value     | Editable hexadecimal input |
| Action        | WRITE button               |

Example:

```text
FREQLO1   0x00   0x00   [34]   [WRITE]
```

---

# 15. Value Formatting

All displayed hexadecimal values use:

* uppercase formatting,
* two-digit fixed-width formatting,
* `0x` prefix.

Examples:

```text
0x00
0x7F
0xFF
```

This formatting applies to:

* register addresses,
* current register values.

---

# 16. Hexadecimal Input Rules

The accepted input format is:

```text
Exactly two hexadecimal digits
No 0x prefix
```

Valid examples:

```text
00
7F
A3
FF
```

Invalid examples:

```text
0x7F
F
123
GG
```

The input field:

* automatically normalizes input to uppercase,
* limits input length to exactly two hexadecimal digits.

Invalid input triggers a popup dialog.

---

# 17. WRITE Interaction Workflow

The WRITE operation can be triggered by:

* pressing the WRITE button,
* pressing ENTER inside the input field.

Workflow:

```text
1. Validate input
2. Convert hexadecimal text to byte value
3. Notify application controller
4. Controller updates internal register cache
5. Controller calls:
   write(register, data)
6. Serial service transmits packet
7. GUI current-value display updates
```

After a successful WRITE:

* the input field remains unchanged.

---

# 18. Register Cache

Because the hardware device is write-only:

* the application maintains the authoritative register state internally,
* the GUI reflects the cached software state.

The “Current Value” display represents:

* the last successfully transmitted value.

---

# 19. Reusable Register Widget Concept

Each register widget is reusable and independent.

A register widget is responsible for:

* displaying register information,
* validating user input,
* collecting hexadecimal values,
* emitting write requests.

A register widget is not responsible for:

* serial communication,
* packet construction,
* UART management,
* application logic.

---
