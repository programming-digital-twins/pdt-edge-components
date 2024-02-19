# Programming Digital Twins - Edge Components
This is the source repository for edge-based software components (written primarily in Python [3]) related to my Digital Twins Programming course at Northeastern University. The intent of this repository is to provide students with a baseline edge application / compute capability that can serve as the data generator and hardware 'emulation' functionality for the digital twin components (which are housed in a separate repository). For convenience to the reader, much of the basic functionality has already been implemented (such as configuration logic, consts, interfaces, and test cases).

These classes and their relationships respresent a notional design that aligns with the requirements listed in [Programming Digital Twins Requirements](https://github.com/orgs/programming-digital-twins/projects/1). These requirements encapsulate the programming exercises presented in my course [Buliding Digital Twins](TBD).

## Links, Exercises, Updates, Errata, and Clarifications

Please see the following links to access exercises for this project. Please note that many of the exercises and sample source code in this repository is based on the Constrained Device Application design and exercises from my book, [Programming the Internet of Things Book](https://learning.oreilly.com/library/view/programming-the-internet/9781492081401/).
 - [Programming Digital Twins Requirements](https://github.com/orgs/programming-digital-twins/projects/1)
 - [Original Constrained Device Application Source Code Template](https://github.com/programming-the-iot/python-components)
 - [Programming the Internet of Things Book](https://learning.oreilly.com/library/view/programming-the-internet/9781492081401/)

## How to use this repository
If you're reading [Programming the Internet of Things: An Introduction to Building Integrated, Device to Cloud IoT Solutions](https://learning.oreilly.com/library/view/programming-the-internet/9781492081401), you'll see a partial tie-in with the exercises described in each chapter and this repository.

## This repository aligns to exercises in Programming Digital Twins, and partially to Programming the Internet of Things
These components are all written in Python 3, and are largely based on, although different from, the exercises designed for the Constrained Device Application (CDA) specified in my book [Programming the Internet of Things: An Introduction to Building Integrated, Device to Cloud IoT Solutions](https://learning.oreilly.com/library/view/programming-the-internet/9781492081401).

## How to navigate the directory structure for this repository
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

# Other things to know

## Pull requests
PR's are disabled while the codebase is being developed.

## Updates
Much of this repository, and in particular unit and integration tests, will continue to evolve, so please check back regularly for potential updates. Please note that API changes can - and likely will - occur at any time.

# REFERENCES
This repository has external dependencies on other open source projects. I'm grateful to the open source community and authors / maintainers of the following libraries:

Core exercises:

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

# FAQ
For typical questions (and answers) to the repositories of the Programming the IoT project, please see the [FAQ](https://github.com/programming-the-iot/book-exercise-tasks/blob/default/FAQ.md).

# IMPORTANT NOTES
This code base is under active development.

If any code samples or other technology this work contains, describes, and / or is subject to open source licenses or the intellectual property rights of others, it is your responsibility to ensure that your use thereof complies with such licenses and/or rights.

# LICENSE
Please see [LICENSE](https://github.com/programming-digital-twins/pdt-edge-components/blob/alpha/LICENSE) if you plan to use the non-code resources (sample data files, etc.)
Please see [LICENSE-CODE](https://github.com/programming-digital-twins/pdt-edge-components/blob/alpha/LICENSE-CODE) if you plan to use this code (e.g., Python code, etc.)
