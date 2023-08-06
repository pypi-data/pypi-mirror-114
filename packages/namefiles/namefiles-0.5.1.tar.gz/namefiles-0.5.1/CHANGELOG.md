# Changelog
This changelog is inspired by [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [0.5.1] - 2021-04-28
### Fixed
- Fixed a bug within the filename convention lead to the source_id mismatching 
  with the sub_id.
- Bad formatting of the FilenameParts class docstring for the documentation.
  
### Changed
- Refined code of the function *disassemble_filename*

## [0.5.0] - 2021-04-01
### Added
- class *FilenameParts* will replace *FilenameParts* in the next minor release.
- more tests

## [0.4.0] - 2021-04-01
### Added
- Functions *is_a_filename_part*, *extract_filename_parts*

### Fixed
- Incorrect dependencies in tox.ini
- Wrong regex within documentation.

### Changed
- Method *FilenameParts.set_parts* now only set and uses parts, which comply with its
  file name convention.

## [0.3.0] - 2021-03-05
### Added
- A lot more tests and docstrings.
- functions *get_filename_convention* and *get_filename_validator* to encapsulate
  the standard file naming convention.
- Most of the documentation.

## [0.2.0] - unreleased
### Changed
- opened the context length from 3-4 to 3-12

## [0.1.0] - unreleased
### Changed
- renamed *ANameGiver.as_path* to *ANameGiver.to_path* and adding the option to
  define a root path for the file.
- *ANameGiver.disassemble* now always defines a *root_path*. It is either the supplied
  filepath's root path or the current working directory.

## [0.0.2] - unreleased
### Changed
- *disassemble_filename* replaces *disassemble_name* for better context.

### Fixed
- Bug in *disassemble_filename* if no filename validator is supplied. 

## [0.0.1] - unreleased
Start of namefiles.
