# SimpleScalar OoO CPU Configuration File Generator

### Overview

This repository generates a configuration file for an out-of-order superscalar processor. The configuration file is used by the [SimpleScalar](http://www.simplescalar.com/) CPU simulator to obtain the average MIPS rate by which the processor can run a series of testbench files. Ultimately, the goal is to refine the parameters of the configuration file such that the MIPS rate is maximized.  

The process of generating a configuration file requires the following steps: 

1. Define initial configuration file parameters, such as L1 and L2 cache sizes, machine width, cache replacement strategies, etc. 
2. Use Real Estimator, an MS Excel-based hardware complexity estimation tool that computes transistor count, area, etc. 
3. Use Cacti, a web-based tool that estimates access times and power consumption of CPU structures that store data.
4. Compile all the results into a configuration file for the SimpleScalar CPU simulation. 

This process is tedious, particularly when refining the parameters may require hundreds of configuration file iterations. Thus, the scripts in this repository automatically performs all these steps.

### Tech

The scripts in this project are written in Python and the following libraries to perform the required objectives: 

- [xlwings](https://www.xlwings.org/) - realtime reading and writing of Excel documents
- [mechanize](http://wwwsearch.sourceforge.net/mechanize/) - stateful programmatic web browsing

### Usage

Generate a configuration file: `python get_config.py <config-name>`
