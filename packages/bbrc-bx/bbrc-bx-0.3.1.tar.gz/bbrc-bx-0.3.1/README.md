# bx

[![pipeline status](https://gitlab.com/xgrg/bx/badges/master/pipeline.svg)](https://gitlab.com/xgrg/bx/commits/master)
[![coverage report](https://gitlab.com/xgrg/bx/badges/master/coverage.svg)](https://gitlab.com/xgrg/bx/commits/master)
[![downloads](https://img.shields.io/pypi/dm/bbrc-bx.svg)](https://pypi.org/project/bbrc-bx/)
[![python versions](https://img.shields.io/pypi/pyversions/bbrc-bx.svg)](https://pypi.org/project/bbrc-bx/)
[![pypi version](https://img.shields.io/pypi/v/bbrc-bx.svg)](https://pypi.org/project/bbrc-bx/)

BarcelonaBeta + XNAT = BX

The interested reader may find a description of `bx` in its native ecosystem in [J. Huguet et al.](https://www.frontiersin.org/articles/10.3389/fnins.2021.633438/full), _Frontiers in Neuroscience_ (2021) (doi:[10.3389/fnins.2021.633438](https://www.frontiersin.org/articles/10.3389/fnins.2021.633438/full)).


## Example:

![example](https://gitlab.com/xgrg/tweetit/raw/master/resources/004-Collecting-FreeSurfer-data-from-XNAT.gif)

## Usage

```
bx <command> <subcommand> <resource_id> --config /path/to/.xnat.cfg --dest /tmp
```

`resource_id` may be a reference to a whole XNAT project, some specific imaging
session (as found in the table returned by `bx id PROJECT_ID`) or a 'list' of
sessions (a list of existing lists may be obtained by `bx lists show`).


### **`ANTS`**:

ANTS - Advanced Normalization Tools

    Available subcommands:
     `files`:           download all `ANTS` outputs
     `snapshot`:        download a snapshot from the `ANTS` pipeline
     `report`:          download the validation report issued by `ANTSValidator`
     `tests`:           creates an Excel table with all automatic tests outcomes from `ANTSValidator`

    Usage:
     bx ants <subcommand> <resource_id>

### **`ARCHIVING`**:

Archiving - used to collect automatic tests from `ArchivingValidator`

    Available subcommands:
     `tests`:           creates an Excel table with all automatic tests outcomes from `ArchivingValidator`

    Usage:
     bx archiving <subcommand> <resource_id>

### **`ASHS`**:

ASHS (Hippocampal subfield segmentation)

    Available subcommands:
     `files`:           download all `ASHS` outputs (segmentation maps, volumes, everything...)
     `volumes`:         creates an Excel table with all hippocampal subfield volumes
     `snapshot`:        download a snapshot from the `ASHS` pipeline
     `report`:          download the validation report issued by `ASHSValidator`
     `tests`:           creates an Excel table with all automatic tests outcomes from `ASHSValidator`

    Usage:
     bx ashs <subcommand> <resource_id>

### **`BAMOS`**:

BAMOS (Bayesian MOdel Selection for white matter lesion segmentation)

    Available subcommands:
     `files`:           download all `BAMOS` outputs
     `volumes`:         create an Excel table with global lesion volumes
     `layers`:          download `layer` (i.e. depth) maps
     `lobes`:           download lobar segmentation maps
     `stats`:           create an Excel table with lesions stats per lobe and depth
     `snapshot`:        download a snapshot from the `BAMOS` pipeline
     `report`:          download the validation report issued by `BAMOSValidator`

    Usage:
     bx bamos <subcommand> <resource_id>

    References:
    - Sudre et al., IEEE TMI, 2015

### **`BRAAK`**:

Extract morphometric/metabolic measurements based on Braak staging.

    Morphometric values are based on regional volumes or cortical thickness
    as estimated individually by FreeSurfer with respect to each specific stage
     (namely, Braak_I_II, Braak_III_IV and Braak_V_VI). For each of them, the
    mean value in all the regions related to the specific stage is returned.

    Metabolic data refer to FDG update associated with each stage as defined
    by their corresponding ROIs. Masks of each stage were defined based on the
    CerebrA atlas (Manera et al.).

    Available subcommands:
     `volumes`:         creates an Excel table with regional volumes for each stage
     `thickness`:       creates an Excel table with cortical thickness for each stage
     `fdg`:             creates an Excel table with the FDG uptake for each stage

    Usage:
     bx braak <subcommand> <resource_id>

    References:
    - Braak et al., Acta Neuropathol. 2006
    - Schöll et al., Neuron. 2016
    - Manera et al.,  Scientific Data. 2020

### **`CAT12`**:

CAT12 - Gray/white matter segmentation

    Available subcommands:
     `files`:           download all `CAT12` outputs (segmentation maps, warp fields, everything...)
     `volumes`:         creates an Excel table with GM/WM/CSF volumes
     `snapshot`:        download a snapshot from the segmentation results
     `report`:          download the validation report issued by `CAT12Validator`
     `tests`:           creates an Excel table with all automatic tests outcomes from `CAT12Validator`

    Usage:
     bx cat12 <subcommand> <resource_id>

### **`DONSURF`**:

DONSURF - Diffusion ON SURFace

    Available subcommands:
     `files`:           download all `recon-all` outputs (segmentation maps, files, everything...)
     `aparc`:           create an Excel table with all `aparc` measurements
     `snapshot`:        download a snapshot from the `recon-all` pipeline
     `report`:          download the validation report issued by bbrc-validator
     `tests`:           create an Excel table with all automatic tests outcomes from bbrc-validator

    Usage:
     bx donsurf <subcommand> <resource_id>

### **`DTIFIT`**:

Processing of Diffusion-weighted Imaging data

    Available subcommands:
    `maps`:             download parametric maps (FA, MD, AxD, RD)
    `files`:            download all outputs from the `DTIFIT` pipeline (up to parametric maps)
    `report`:           download the validation report issued by `DTIFITValidator`
    `snapshot`:         download a snapshot with FA map, RGB tensor and TOPUP distortion correction map

    Usage:
     bx dtifit <subcommand> <resource_id>

### **`FREESURFER6`**:

FreeSurfer v6.0.0

    Available subcommands:
     `files`:           download all `recon-all` outputs (segmentation maps, files, everything...)
     `aseg`:            create an Excel table with all `aseg` measurements
     `aparc`:           create an Excel table with all `aparc` measurements
     `hippoSfVolumes`:  save an Excel table with hippocampal subfield volumes (if available)
     `snapshot`:        download a snapshot from the `recon-all` pipeline
     `report`:          download the validation report issued by bbrc-validator
     `tests`:           create an Excel table with all automatic tests outcomes from bbrc-validator

    Usage:
     bx freesurfer6 <subcommand> <resource_id>

### **`FREESURFER6HIRES`**:

FreeSurfer v6.0.0 (-hires option)

    Available subcommands:
     `files`:           download all `recon-all` outputs (segmentation maps, files, everything...)
     `aseg`:            create an Excel table with all `aseg` measurements
     `aparc`:           create an Excel table with all `aparc` measurements
     `hippoSfVolumes`:  save an Excel table with hippocampal subfield volumes (if available)
     `snapshot`:        download a snapshot from the `recon-all` pipeline
     `report`:          download the validation report issued by bbrc-validator
     `tests`:           create an Excel table with all automatic tests outcomes from bbrc-validator

    Usage:
     bx freesurfer6hires <subcommand> <resource_id>

### **`FREESURFER7`**:

FreeSurfer v7.1.1

    Available subcommands:
     `files`:           download all `recon-all` outputs (segmentation maps, files, everything...)
     `aseg`:            create an Excel table with all `aseg` measurements
     `aparc`:           create an Excel table with all `aparc` measurements
     `hippoSfVolumes`:  save an Excel table with hippocampal subfield volumes (if available)
     `snapshot`:        download a snapshot from the `recon-all` pipeline
     `report`:          download the validation report issued by bbrc-validator
     `tests`:           create an Excel table with all automatic tests outcomes from bbrc-validator

    Usage:
     bx freesurfer7 <subcommand> <resource_id>

### **`ID`**:

Return generic information like subject/session labels, parent project.

    Usage:
     bx id <resource_id>

### **`LISTS`**:

Manage experiment lists curated by BarcelonaBeta.

    Available subcommands:
     `show`:            display all existing lists (usage: bx lists show)

    Usage:
     bx lists <subcommand>

### **`NIFTI`**:

Download NIfTI images from a given sequence (`SeriesDesc`).

    Available subcommands:
     `usable`:          download `usable` images (default)
     `all`:             download all images found
    User is then asked for sequence name (ex: T1, T2, DWI). Has to match with
    the one in XNAT (wildcards accepted).

    Usage:
     bx nifti <subcommand> <resource_id>

### **`FDG`**:

18F-fluorodeoxyglucose PET imaging data

    Available subcommands:
     `landau`:          creates an Excel table with the Landau's metaROI signature
     `maps`:            download the normalized FDG maps
     `tests`:           collect all automatic tests outcomes from `FDGQuantiticationValidator`

    Usage:
     bx fdg <subcommand> <resource_id>

    Reference:
    - Landau et al., Ann Neurol., 2012

### **`FTM`**:

18F-flutemetamol PET imaging data

    Available subcommands:
     `centiloids`:      creates an Excel table with centiloid scales
     `maps`:            download the normalized FTM maps
     `tests`:           collect all automatic tests outcomes from `FTMQuantiticationValidator`

    Usage:
     bx ftm <subcommand> <resource_id>

    References:
     - Klunk et al, Alzheimers Dement., 2015

### **`SCANDATES`**:

Collect acquisition dates from imaging sessions.

    Usage:
     bx scandates <resource_id>

### **`SIGNATURE`**:

Download composite measurements labeled as 'signatures' of Alzheimer's Disease

    Available subcommands:
     `jack`:            based on FreeSurfer's cortical thickness and local cortical gray matter volumes
     `dickerson`:       based on Dickerson's cortical signatures (see references below)

    Usage:
     bx signature <subcommand> <resource_id>

    Jack's AD signature is calculated in two versions,
    weighted and not weighted. Weighted means that the formula has been
    applied by normalizing each ROI value by local surface area (as explained
    in the papers).
    Not-weighted versions correspond to mean values across regions.

    Examples:

    `bx signature jack` will return Jack's signature, based on thickness and grayvol values.
    `bx signature dickerson` will return AD and aging signatures, based only on
    thickness values as they do not have any "grayvol" version.

    References:
    - Jack et al., Alzheimers Dement. 2017
    - Dickerson et al., Neurology, 2011
    - Bakkour et al., NeuroImage, 2013

### **`SPM12`**:

SPM12 - Gray/white matter segmentation

    Available subcommands:
     `files`:           download all `SPM12` outputs (segmentation maps, warp fields, everything...)
     `volumes`:         creates an Excel table with GM/WM/CSF volumes
     `snapshot`:        download a snapshot from the segmentation results
     `report`:          download the validation report issued by `SPM12Validator`
     `tests`:           creates an Excel table with all automatic tests outcomes from `SPM12`
     `rc`:              downloads rc* files (DARTEL imports)

    Usage:
     bx spm12 <subcommand> <resource_id>


## Dependencies

Requires [`bbrc-pyxnat>=1.4.2`](https://gitlab.com/pyxnat/pyxnat/tree/bbrc) and
the librairies listed in `requirements.txt`.


## Install

```
pip install bbrc-bx
```

## Development

Please contact us for details on how to contribute.

[![BarcelonaBeta](https://www.barcelonabeta.org/sites/default/files/logo-barcelona-beta_0.png)](https://www.barcelonabeta.org/)
