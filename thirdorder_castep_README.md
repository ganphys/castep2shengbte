# Manual for thirdorder_castep.py 

This directory contains CASTEP interface files to the thirdorder package. It calculates the third order force contants. The interface allows the user to generate the `FORCE_CONSTANTS_3RD` file, which is needed to run ShengBTE.
The thirdorder package is NOT part of CASTEP and the CASTEP authors are not responsible for it.
You can find further information on ShengBTE and thirdorder.py, including features and downloads, at http://www.shengbte.org/home

## Getting Started

Please read the main thirdorder.py README before trying to use it with CASTEP! 

You can obtained the interface either as part of the CASTEP distribution, or download the most recent version from https://github.com/ganphys/castep2shengbte

The current version of the interface (thirdorder_castep.py) is compatible with thirdorder v.1.0.2 (most recent version).

### Prerequisites

Install thirdorder-v1.0.2 (you can download it from the ShengBTE [website](http://www.shengbte.org/downloads)) and then put thirdorder_castep.py in the installation directory

## Using thirdorder_castep.py with CASTEP

### SOW mode:
 	Input files: <seedname>.cell, <seedname>.param

	Output files: <seedname>-3RD directory, which countains multiple job-<number> subdirectories. 
       	Each subdirectory contains a supercell <seedname>.cell file with a small perturbation and a copy of the <seedname>.param file.

	command: `thirdorder_castep.py sow nx ny nz cutoff seedname` 
 	Example: `thirdorder_castep.py sow 1 1 1 -3 InAs`

It is necessary to complete all jobs in `<seedname>`-3RD directory before proceeding to REAP mode. 

### REAP mode:
	Input files: <seedname>.castep (thirdorder_castep.py goes through all subdirectories in <seedname>-3RD and collects forces data.)
 
	Output file: FORCE_CONSTANTS_3RD

	command: `find <seedname>-3RD/job* -name <seedname>.castep | sort -n| thirdorder_castep.py reap nx ny nz cutoff seedname`
 	Example: `find InAs-3RD/job* -name InAs.castep | sort -n| thirdorder_castep.py reap 1 1 1 -3 seedname`

Use FORCE_CONSTANTS_3RD file along with FORCE_CONSTANTS_2ND and CONTROL to perform a ShengBTE run.

### LIMITATIONS: 
- It is not possible to do spin polarised calculations because spin will not be included in the supercell files.

- Initial <seedname>.cell file MUST be in the following format:
	  Lattice parameter, Cell contents AND THEN everything else.
- Absolute coordinates are not supported.

### Useful tips

- Use `write_checkpoint: none` in the `<seedname>`.param file. Otherwise, the process of writing hunderds of checkpoint files to the hard drive will slow down the calculation process.
 
- It is possible to reuse a single checkpoint file for each of the runs. This should save you a couple of hours. For that purpose generate a checkpoint file from one of the runs and place the file in the root directory where your input files are placed. Then add `reuse : ../../seedname.check` to your `<seedname>`.param file in the root directory and either run once again thirdorder_castep.py in SOW mode paste the edited `<seedname>`.param file to all subdirectories or copy and paste it manually.

- If you don't want to generate the pseudopotentials at the start of each run, you can add the following block to the end of the <seedname>.cell in the root directory:

```
%BLOCK SPECIES_POT
Fe ../../Fe_C17_PBE_OTF.usp
Ta ../../Ta_C17_PBE_OTF.usp
Sb ../../Sb_C17_PBE_OTF.usp
%ENDBLOCK SPECIES_POT
```

Please note that you need to edit the elements and the name of the pseudopotentials in accordance to your system.

## Author

* **Genadi Naydenov** - (https://github.com/ganphys/castep2shengbte)

