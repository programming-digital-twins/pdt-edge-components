# Programming Digital Twins - Edge Components

## Overview

This is the source repository for edge-based software components (written primarily in Python 3) related to my Digital Twins Programming course at Northeastern University. The intent of this repository is to provide students with a baseline edge application / compute capability that can serve as the data generator and hardware 'emulation' functionality for the digital twin components (which are housed in a separate repository). For convenience to the reader, much of the basic functionality has already been implemented (such as configuration logic, consts, interfaces, and test cases).

These classes and their relationships respresent a notional design that aligns with the requirements listed in [Programming Digital Twins Requirements](https://github.com/orgs/programming-digital-twins/projects/1). These requirements encapsulate the programming exercises presented in my Northeastern University course Building Digital Twins.

### Project Objectives

The [LabBenchStudios-PDT-Unity](https://github.com/programming-digital-twins/LabBenchStudios-PDT-Unity) project is intended to be used with [pdt-eda-components](https://github.com/programming-digital-twins/pdt-eda-components) and repository has three primary objectives:

(1) Build a largely F/OSS Digital Twin framework that can work with other [Programming Digital Twins projects](https://github.com/programming-digital-twins) and their repositories to sync live data, DTDL models, and a JSON-based constraint mapping layer, and render within a COTS physics sim engine (e.g., Unity 6).

(2) Use a digital twin asset's configuration data to auto-generate a GPT AI prompt to query one or more locally running LLM's to retrieve predictive maintenance recommendations for the specific system within the Digital Twin environment.

(3) Provide a baseline technology platform for my Northeastern University College of Engineering graduate students (and me) to learn and experiment with various Digital Twin use cases.

### Helpful Links

PDT Kanban Board: [Programming Digital Twins Requirements](https://github.com/orgs/programming-digital-twins/projects/1)

Please see the following links for some helpful information about the PDT exercises and other associated repositories. Please note that many of the exercises and sample source code in this repository is based on some of the patterns and exercises from my book, [Programming the Internet of Things Book](https://learning.oreilly.com/library/view/programming-the-internet/9781492081401/).
 - Programming Digital Twins (PDT) specific:
   - [Programming Digital Twins Exercises (aka PDT Kanban Board)](https://github.com/orgs/programming-digital-twins/projects/1)
   - [Programming Digital Twins - LBS PDT Unity Package](https://github.com/programming-digital-twins/LabBenchStudios-PDT-Unity/)
   - [Programming Digital Twins Client Framework Repository](https://github.com/programming-digital-twins/pdt-cfw-components)
   - [Programming Digital Twins Edge Components Repository](https://github.com/programming-digital-twins/pdt-edge-components)
   - [Programming Digital Twins Exercise Doc Templates Repository](https://github.com/programming-digital-twins/pdt-exercise-docs)
 - Other reading links:
   - [Programming the Internet of Things Exercises (aka PIOT Kanban Board)](https://github.com/orgs/programming-the-iot/projects/5)
   - [Programming the Internet of Things Book](https://learning.oreilly.com/library/view/programming-the-internet/9781492081401/)

## Usage

### Installation

NOTE: See the instructions listed in [PDT-EDA-01-001](https://github.com/programming-digital-twins/pdt-exercise-tasks/issues/23) for details.

#### In Summary

- From the command line using git and pip (NOTE: path names are examples only - yours will likely differ)
  - Clone the repository: Use `git clone` with this repository's git URL.
  - Setup and activate a Python virtual env: See Chapter 1, Step I.6 (Set up your Python environment) from [Programming the Internet of Things](https://learning.oreilly.com/library/view/programming-the-internet/9781492081401/ch01.html). The repository is different but the steps are very similar for the edge device app (EDA) as they are for the book's constrained device app (CDA).
  - Set your PYTHONPATH: It should include both the main and test paths. For example (NOTE: your local path may be different):
    - E.g., `export PYTHONPATH=/mnt/d/pdt/pdt-edge-components/src/main/python:/mnt/d/pdt/pdt-edge-components/src/test/python`
  - Install the dependencies: Use `pip install -r requirements.txt` to install the relevant dependencies.

### Running the EDA from the Command Line

- From the command line using Python (NOTE: path names are examples only - yours will likley differ)
  - Update the config: If necessary, edit the `PdtConfig.props` config file in the ./config path and set the `enableMqttClient = True` entry to False: `enableMqttClient = False`. This can be changed later once your MQTT broker is running and reachable from the app.
  - Run the app: `python /mnt/d/pdt/pdt-edge-components/src/main/python/labbenchstudios/pdt/edge/app/EdgeDeviceApp.py -c /mnt/d/pdt/pdt-edge-components/config/PdtConfig.props`
  - It will take a short time to initialize and start - you should see the simulator kick-off and start generating sample data. Here's an abbreviated example:
```
2025-01-02 11:59:27,719:::140498646437888:root.EdgeDeviceApp.main()[111]:INFO:Parsed configuration file arg: /mnt/d/pdt/eda005/PdtConfig.props
2025-01-02 11:59:27,719:::140498646437888:root.ConfigUtil.__init__()[60]:INFO:Creating instance of ConfigUtil: /mnt/d/pdt/eda005/PdtConfig.props
2025-01-02 11:59:27,721:::140498646437888:root.ConfigUtil._loadConfigFile()[239]:INFO:Attempting to load config file: /mnt/d/pdt/eda005/PdtConfig.props
2025-01-02 11:59:27,723:::140498646437888:root.ConfigUtil._loadConfigFile()[248]:INFO:Successfully loaded configuration at /mnt/d/pdt/eda005/PdtConfig.props.
.
.
.
2025-01-02 11:59:27,819:::140498646437888:root.DeviceDataManager._initManager()[418]:INFO:Local sensor tracking enabled
2025-01-02 11:59:27,820:::140498646437888:root.DeviceDataManager._initManager()[422]:INFO:Local actuation capabilities enabled
2025-01-02 11:59:27,820:::140498646437888:root.EdgeDeviceApp.startApp()[66]:INFO:Starting EDA...
2025-01-02 11:59:27,820:::140498646437888:root.DeviceDataManager.startManager()[328]:INFO:Starting DeviceDataManager...
2025-01-02 11:59:27,820:::140498646437888:root.DeviceDataManager.startManager()[333]:INFO:Starting event dispatch manager...
2025-01-02 11:59:27,820:::140498646437888:root.EventDispatchManager.startManager()[180]:INFO:Starting EventDispatchManager...
2025-01-02 11:59:27,820:::140498646437888:root.EventDispatchManager.startManager()[183]:INFO:Starting message queue processor thread...
2025-01-02 11:59:27,820:::140498646437888:root.EventDispatchManager.startManager()[186]:INFO:Started EventDispatchManager.
.
.
.
2025-01-02 11:59:27,829:::140498646437888:root.DeviceDataManager.startManager()[351]:INFO:Started DeviceDataManager.
2025-01-02 11:59:27,830:::140497507055168:apscheduler.scheduler.base._process_jobs()[1023]:DEBUG:Next wakeup is due at 2025-01-02 11:59:57.818632-05:00 (in 29.988570 seconds)
2025-01-02 11:59:27,830:::140498646437888:root.EdgeDeviceApp.startApp()[74]:INFO:EDA started.
```

- Once the app is configured and the initial test run is successful, follow the exercises in [Programming Digital Twins Kanban Board Exercises](https://github.com/orgs/programming-digital-twins/projects/1) to configure the remaining components (e.g., MQTT broker, DTA, etc.)

Note: Check back regularly for version updates, as this repository is under active development and is in 'alpha' mode (e.g., UNRELEASED).

## Organization

If you're reading [Programming the Internet of Things: An Introduction to Building Integrated, Device to Cloud IoT Solutions](https://learning.oreilly.com/library/view/programming-the-internet/9781492081401), you'll see a partial tie-in with the exercises described in each chapter and this repository.

Please NOTE: This repository aligns to exercises in Programming Digital Twins, and partially to Programming the Internet of Things

These components are all written in Python 3, and are largely based on, although different from, the exercises designed for the Constrained Device Application (CDA) specified in my book [Programming the Internet of Things: An Introduction to Building Integrated, Device to Cloud IoT Solutions](https://learning.oreilly.com/library/view/programming-the-internet/9781492081401).

### Repository Navigation

This repository is comprised of the following top level paths:
- [config](https://github.com/programming-digital-twins/pdt-edge-components/tree/alpha/config): Contains basic configuration file(s).
- [src](https://github.com/programming-digital-twins/pdt-edge-components/tree/alpha/src): Contains the following source trees:
  - [src/main/python](https://github.com/programming-digital-twins/pdt-edge-components/tree/alpha/src/main/python): The main source tree for python-components. Keep in mind that most of these classes are shell representations ONLY and must be implemented as part of the exercises referenced above.
  - [src/test/python](https://github.com/programming-digital-twins/pdt-edge-components/tree/alpha/src/test/python): The test source tree for python-components. These are designed to perform very basic unit and integration testing of the implementation of the exercises referenced above. This tree is sectioned by part - part01, part02, and part03 - which correspond to the structure of Programming the Internet of Things.
- [simTestData](https://github.com/programming-digital-twins/pdt-edge-components/tree/alpha/simTestData): Contains sample simulated test data.
  - This simulated test data was generated as part of my own solution to Lab Module 5 as part of the exercises referenced above. Keep in mind that these data are from my own solution, which will likely be different from your own.

Here are some other files at the top level that are important to review:
- [requirements.txt](https://github.com/programming-digital-twins/pdt-edge-components/blob/alpha/requirements.txt): The core library dependencies - use pip to install.
- [README.md](https://github.com/programming-digital-twins/pdt-edge-components/blob/alpha/README.md): This README.
- [LICENSE](https://github.com/programming-digital-twins/pdt-edge-components/blob/alpha/LICENSE): The repository's non-code artifact LICENSE file (e.g., documentation, sample data files, etc.)
- [LICENSE-CODE](https://github.com/programming-digital-twins/pdt-edge-components/blob/alpha/LICENSE-CODE): The repository's code artifact LICENSE file (e.g., source code [mostly Python])

Lastly, here are some 'dot' ('.{filename}') files pertaining to dev environment setup that you may find useful (or not - if so, just delete them after cloning the repo):
- [.gitignore](https://github.com/programming-digital-twins/pdt-edge-components/blob/alpha/.gitignore): The obligatory .gitignore that you should probably keep in place, with any additions that are relevant for your own cloned instance.
- [.project](https://github.com/programming-digital-twins/pdt-edge-components/blob/alpha/.project): The Eclipse IDE project configuration file that may / may not be useful for your own cloned instance. Note that using this file to help create your Eclipse IDE project will result in the project name 'piot-python-components' (which can be changed, of course).
- [.pydevproject](https://github.com/programming-digital-twins/pdt-edge-components/blob/alpha/.pydevproject): The Eclipse IDE and PyDev-specific configuration file for your Python environment that may / may not be useful for your own cloned instance.

NOTE: The directory structure and all files are subject to change based on feedback I receive from readers of my book and students in my IoT class, as well as improvements I find to be helpful for overall repo betterment.

## Other things to know

### Pull requests

PR's are disabled while the codebase is being developed.

### Updates

Much of this repository, and in particular unit and integration tests, will continue to evolve, so please check back regularly for potential updates.
Please note that API changes can - and likely will - occur at any time.

# REFERENCES

This repository has external dependencies on other open source projects. I'm grateful to the open source community and authors / maintainers of the following libraries:

- [apscheduler](https://github.com/agronholm/apscheduler)
  - Reference: A. Grönholm. APScheduler. (2020) [Online]. Available: https://pypi.org/project/APScheduler/.
- [psutil](https://github.com/giampaolo/psutil)
  - Reference: G. Rodola. Psutil. (2009 – 2020) [Online]. Available: https://psutil.readthedocs.io/en/latest/.
- [numpy](https://numpy.org/)
  - Reference: NumPy. NumPy. (2020) [Online]. Available: https://numpy.org/.
- [matplotlib](https://matplotlib.org/)
  - Reference: [J. D. Hunter, "Matplotlib: A 2D Graphics Environment", Computing in Science & Engineering, vol. 9, no. 3, pp. 90-95, 2007.](https://ieeexplore.ieee.org/document/4160265)
  - DOI: https://doi.org/10.5281/zenodo.592536
- [Sense-Emu](https://sense-emu.readthedocs.io/en/v1.1/)
  - Reference: The Raspberry Pi Foundation. Sense HAT Emulator. (2016) [Online]. Available: https://sense-emu.readthedocs.io/en/v1.0/.
- [pisense](https://pisense.readthedocs.io/en/release-0.2/#)
  - Reference: D. Jones. Pisense. (2016 – 2018) [Online]. Available: https://pisense.readthedocs.io/en/release-0.2/.
- [paho-mqtt](https://www.eclipse.org/paho/)
  - Reference: Eclipse Foundation, Inc. Eclipse Paho™ MQTT Python Client. (2020) [Online]. Available: https://github.com/eclipse/paho.mqtt.python.
- [influxdb-client-python](https://github.com/influxdata/influxdb-client-python)
  - Reference: InfluxData. Influx DB Python Client. (2023) [Online]. Available: https://github.com/influxdata/influxdb-client-python.

NOTE: This list will be updated as others are incorporated.

# IMPORTANT NOTES

This code base is under active development.

If any code samples or other technology this work contains, describes, and / or is subject to open source licenses or the intellectual property rights of others, it is your responsibility to ensure that your use thereof complies with such licenses and/or rights.

# LICENSE

- Docs and configuration files: See [LICENSE-DATA](https://github.com/programming-digital-twins/pdt-edge-components/blob/alpha/LICENSE-DATA.md) if you plan to use the non-code resources (i.e., sample JSON data files and JSON configuration file).

- Source code files (Python): See [LICENSE-CODE](https://github.com/programming-digital-twins/pdt-edge-components/blob/alpha/LICENSE-CODE.md) if you plan to use this code (i.e., Python code).
