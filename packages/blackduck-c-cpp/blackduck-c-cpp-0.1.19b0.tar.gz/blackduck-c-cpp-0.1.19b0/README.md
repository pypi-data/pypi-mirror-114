# blackduck-c-cpp

This code is responsible for running a c/cpp build wrapped by Coverity - capturing the source and binary files involved and then using the available tools to deliver BDIO and signatures to Black Duck using a variety of tools and methodologies.

## Overview
C and CPP projects don't have a standard package manager or method for managing dependencies.  It is therefore more difficult to create an accurate BOM for these projects.  This leaves Software Composition Analysis tools fewer options than with other languages.  The primary options which are available in this context are: file system signatures.  Black Duck has a variety of old and new signatures which can be used to build a BOM.  In order to effectively use signatures, the tool first needs to know which files to take signatures from.  In the past SCA tools have pointed a scanner at a build directory, getting signatures from a subset of files within the directory sub-tree.  The problem with this approach is that there are many environmental variables, parameters and switches provided to the build tools, which make reference to files outside of the build directory to include as part of the build.  Further, there are, commonly, files within the build directory, which are not part of the build and can lead to false positives within the BOM. 

The new Black Duck C/CPP tool avoids the pitfalls described above by using a feature of Coverity called Build Capture.  Coverity Build Capture, wraps your build, observing all invocations of compilers and linkers and storing the paths of all compiled source code, included header files and linked object files.  These files are then matched using a variety of methods described in the section of this document called "The BOM".

## Installation
Minimum version of Black Duck required is 2020.10.0

To install from pypi:
```
pip install blackduck-c-cpp
```

To install a specific version:
```
pip install blackduck-c-cpp==0.1.18b0
```

## Configuration
Prior to running your build, run any build specific configuration needed.  Then the blackduck-c-cpp tool can either be configured using a .yaml file or with command line arguments.

Here is a sample fully functional .yaml configuration: godot-config.yaml

```
build_cmd: scons platform=osx arch=x86_64 --jobs=$(sysctl -n hw.logicalcpu)
build_dir: /Users/theUser/myProject/godot/
coverity_root: /Users/theUser/apps/bds/coverity/
skip_build: False
verbose: True
project_name: godot_mac
project_version: may-4-2021
codelocation_name: godot_mac
bd_url: https://...
api_token: <token>
insecure: False
```

### API Token
To generate an API token:

1. Go to the Black Duck UI and log in.
2. From the user menu located on the top navigation bar, select My Access Tokens. 
3. Click Create New Token. The Create New Token dialog box appears. 
4. Enter a name, description (optional), and select the scope for this token (to use with blackduck-c-cpp, must be **read and write access**). 
5. Click Create. The Access Token Name dialog box appears with the access token.
6. Copy the access token shown in the dialog box. This token can only be viewed here at this time. Once you close the dialog box, you cannot view the value of this token.


### Details

usage: blackduck-c-cpp [-h] [-c CONFIG] -bc BUILD_CMD -d BUILD_DIR -Cov COVERITY_ROOT [-cd [COV_DIR]] [-s [SKIP_BUILD]] [-v [verbose]] -proj PROJECT_NAME -vers PROJECT_VERSION [-Cl CODELOCATION_NAME] -bd bd_url -a 
api_token [-as additional_sig_scan_args] [-i [insecure]] [-djs [DISABLE_JSON_SPLITTER]] [-si SCAN_INTERVAL] [-jsl json_splitter_limit] [-dg [debug]]


arguments:
```
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        Configuration file path.
  -bc BUILD_CMD, --build_cmd BUILD_CMD
                        Command used to execute the build
  -d BUILD_DIR, --build_dir BUILD_DIR
                        Directory from which to run build
  -Cov COVERITY_ROOT, --coverity_root COVERITY_ROOT
                        Base directory for coverity 
  -cd cov_dir, --cov_dir cov_dir
                        Target directory for coverity output files. If not specified, defaults to cov_root/output/project_name directory  
  -s [SKIP_BUILD], --skip_build [SKIP_BUILD]
                        Skip build and use previously generated build data.
  -v [verbose], --verbose [verbose]
                        verbose mode selection
  -proj PROJECT_NAME, --project_name PROJECT_NAME
                        Black Duck project name
  -vers PROJECT_VERSION, --project_version PROJECT_VERSION
                        Black Duck project version
  -Cl CODELOCATION_NAME, --codelocation_name CODELOCATION_NAME
                        Codelocation name
  -bd bd_url, --bd_url bd_url
                        Black Duck URL
  -a api_token, --api_token api_token
                        Black Duck API token
  -as additional_sig_scan_args, --additional_sig_scan_args additional_sig_scan_args
                        Any additional args to pass to the signature scanner
  -i [insecure], --insecure [insecure]
                        Disable SSL verification
  -djs [DISABLE_JSON_SPLITTER], --disable_json_splitter [DISABLE_JSON_SPLITTER]
                        Disable the json splitter and always upload as a single scan
  -si SCAN_INTERVAL, --scan_interval SCAN_INTERVAL
                        Set the number of seconds to wait between scan uploads in case of multiple scans
  -jsl json_splitter_limit, --json_splitter_limit json_splitter_limit
                        Set the limit for a scan size in bytes
  -dg [debug], --debug [debug]
                        Debug mode selection
  -st [SKIP_TRANSITIVES], --skip_transitives [SKIP_TRANSITIVES]
                        Skipping all transitive dependencies
  -sh [SKIP_INCLUDES], --skip_includes [SKIP_INCLUDES]
                        Skipping all .h & .hpp files from all types of scan
  -sd [SKIP_DYNAMIC], --skip_dynamic [SKIP_DYNAMIC]
                        Skipping all dynamic (.so/.dll) files from all types of scan
  -off [OFFLINE], --offline [OFFLINE]
                        store bdba and sig tar files and c_cpp_bdio2.jsonld to disk if offline mode is true
  -md modes, --modes modes
                        comma separated list of modes to run - 'all' - default,'bdba','sig','pkg_mgr'
```

Running
Once your blackduck-c-cpp tool is installed and configured as explained above, simply run the command:

blackduck-c-cpp --config /Users/theUser/myProject/godot-config.yaml

The Bom

Direct Dependencies - These are files which are being linked in to the built executable directly or header files included by source code as identified by Coverity Build Capture.  
Package Manager - The Package Manager of the Linux system is queried about the source of the files - if recognized, these are added to the BOM as "Direct Dependencies".
Transitive Dependencies - These are files which are needed by the Direct Dependencies.
LDD - LDD is used to List the files (Dynamic Dependencies) of the Direct Dependencies.  These files are then used to query the package manager and results are added to the BOM as "Transitive Dependencies".
Binary Matches
BDBA - Any linked object files not identified by the package manager are sent to BDBA (Binary) for matching.
Signature Matches - Any linked object and header files not identified by the package manager as well as all source code identified by Coverity Build Capture are then sent to the Knowledge Base for signature matching.

## CI Builds

This projects CI build is run through GitLab-CI Pipelines, within this repository.  When changes are made on the `master` (default) branch, the version will be appended with `b` and the pipeline number as metadata.  For `release/` branches, `-rc` will be appended to the version with the pipeline number as metadata, and this will be published to Artifactory.  When changes are made to another branch (`dev/` or `bugfix/` for example), `dev` will be appended to the version with the pipeline number, and the commit hash will be appended as metadata.

For example:
* default branch: 1.0.0b3821+abcd1234
* release branch: 1.0.0rc4820+abcd1234
* dev branch: 1.0.0dev5293+abcd1234
* release: 1.0.0

Release jobs are also run through GitLab-CI Pipelines, when tagged as per below.  The version will be uploaded to Artifactory at the end of the pipeline.

# Releasing

To release this library, simply tag this repo with a tag of the format: `vMM.mm.ff` like `v1.0.1`.  This version should match the version (minus the `v` in `setup.py`)

Be sure to increment the version in `setup.py` to the next fix version, or minor/major version as necessary.  Do not add any metadata or additional version information to the version, here.

The specific set of steps is:

- Ensure a full `python setup install` completes
- Commit changes
- Tag with `v##.##.##`, matching the version number in `setup.py`
- Push the change log changes, and tag, to GitLab
- Update the version number in `setup.py`
- Commit version change and push to GitLab
