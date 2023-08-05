# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [0.1.8] - 2021-07-26

### Added

* Package now available to install from conda

## [0.1.7] - 2021-05-18

### Added

* Basic documentation on ReadTheDocs.

## [0.1.6] - 2021-05-15

### Changed

* Change argument names for `BBoxes`: `boxes_coords` -> `bboxes`,  `items_ids` -> `ids` and `labels_conf` -> `scores`.

## [0.1.5] - 2021-04-25

### Fixed

* Improve type checking for integers to take into account numpy integers.

## [0.1.4] - 2021-04-24

### Added

* Throw an error is `boxes` elements in `bboxes_coords` are not integers.
* Explicitly allow numpy array as arguments to `BBoxes.draw`

### Fixed

* Improved check for `None` arguments in `BBoxes`.

## [0.1.3] - 2021-04-04

### Changed

* Change default font sizes for `InfoBox`.

## [0.1.2] - 2021-04-03

### Added

* The `BBoxes`, `InfoBox`,  `Label` and `Font` classes, that can draw bouding objects on the image using custom TrueType fonts.
