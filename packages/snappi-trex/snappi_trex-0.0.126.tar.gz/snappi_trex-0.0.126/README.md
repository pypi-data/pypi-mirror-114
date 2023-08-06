# Snappi-Trex
Snappi-Trex is a Snappi plugin that allows executing scripts written using 
[Snappi](https://github.com/open-traffic-generator/snappi) with Cisco's [T-Rex Traffic Generator](https://trex-tgn.cisco.com)

## Design
Snappi-Trex converts Snappi Open Traffic Generator API configuration into the equivalent T-Rex STL Client configuration. This allows users to use the T-Rex Traffic Generator and its useful features without having to write complex T-Rex scripts. 

![diagram](docs/res/snappi-trex-design.svg)

The above diagram outlines the overall process of how the Snappi Open Traffic Generator API is able to interface with T-Rex and generatee traffic over its network interfaces. Snappi_trex is essential to convert Snappi scripts into the equivalent T-Rex STL Client instructions.

<br>

Snappi_trex usage follows the standard usage of Snappi with a few modifications outlined in the [Usage](https://github.com/open-traffic-generator/snappi-trex/docs/usage.md) document.



# Table of Contents
* [Quickstart](docs/quickstart.md)
* [T-Rex installation and setup](docs/t-rex-tutorial.md)
* [snappi_trex usage](docs/usage.md)
* [snappi_trex full features and limitations](docs/features.md)
* [Testing](docs/testing.md)
* [Contribute](docs/contribute.md)
