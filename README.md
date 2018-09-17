# RoboLab Template

Template for the RoboLab course in spring which is conducted by the Systems Engineering Group at the Department of Computer Science, TU Dresden.

* Acts as a base repository that groups clone and then set the upstream to their assigned repo afterwards.
* Provides scripts to speed up and automate the process of deploying as well as executing Python code on LEGO MINDSTORMS EV3 robots running the customized, Debian based operating system [ev3dev-robolab](https://github.com/7HAL32/ev3dev-robolab).
* Includes the programming interface which is used to check parts of the students solutions in the final exam.


## Workflow

Contains a deploy script that syncs Python files from the local _/src/_ folder to a remote EV3 brick.
This functionality is made available by the submodule [robolab-deploy](https://github.com/7HAL32/robolab-deploy).
Its contents were not directly included in this repository, as the submodule allows easier updating without manually adding files to a groups repository.
Afterwards this scripts attaches to a pre-loaded tmux session on the remote device, which is running `python3.6` including some modules that are already imported. These, for instance the [Python language bindings for the EV3](https://github.com/rhempel/ev3dev-lang-python), usually take way to long for practical development and debugging. The script further performs a reload on the [`main.py`](/src/main.py) file in the remote `/home/robot/src/` folder and starts execution from `main.run()`. This is made possible by the custom systemd service [ev3-robolab-startup](https://github.com/7HAL32/ev3-robolab-startup) that runs automatically on our OS after boot.
Also comes with a simple example `main.py` file that prints `Hello World!` and the programming interface for the corresponding task.
After the exam parts of the solutions of all group repositories will be checked and tested for correctness.

The most recent version regarding the current RoboLab can be found in the `master` branch or a tag, which is named and set according to the current course.


## Installation

These steps should be only performed by **one** member of your group.

#### Clone the repository to any local destination.

```
$ git clone --recursive git clone https://bitbucket.org/SE-Robolab/robolab-template.git
```
The flag `--recursive` initializes the submodule `robolab-deploy`.

#### Change to the working directory.
```
$ cd ./robolab-template
```

#### Set the remote upstream to your group repository.
```
$ git remote set-url origin https://bitbucket.org/robolab-<season>-<year>/group-<id>
```
* `<season>` is either `spring` or `autumn` depending on which RoboLab course you are participating in, i.e. Spring Course (INF) or Autumn Course (NES).
* `<year>` is the year your course has started in the format `yy`. For instance if the introduction took place on March 06th, 2017 `<year>` will be `17`.
* `<id>` has been assigned to you at the beginning of the course. Please make sure to include leading zeros and fill up the id to three digits, e.g. group 42 will enter `042`.

#### Verify, if the new upstream has been set successfully.
```
$ git remote -v
```

#### Perform an initial push.
```
$ git push origin master
```

#### Clone for group members
Now the other members of your team are ready to clone your group repository.
Make sure to enter the corresponding URL from third step and also use the `--recursive` flag.
```
$ git clone --recursive https://bitbucket.org/robolab-<season>-<year>/group-<id>
```


## Dependencies

In order to function you will need to have [Python 3.6](https://www.python.org/downloads/) installed.
All other auxiliary files will be downloaded by the script itself.
On Linux you may also need to install [sshpass](https://gist.github.com/arunoda/7790979) manually.

**Make sure that you are connected to the campus network on the first run to fetch all dependencies.**


## Usage

All source file must reside inside the `src/` sub directory.
To start deploying and executing, call the file according to your operating system configuration and setup of Python.


### Linux and macOS

There is a so called [Shebang](https://en.wikipedia.org/wiki/Shebang_(Unix)) on the top of the scripts.
This should automatically resolve the Python executable in most cases.
```
$ ./deploy.py [optional arguments]
```

### Windows

Unfortunately some investigation and work on Windows may be necessary as the mentioned Shebang does not work here.
```
PYTHON_EXECUTABLE ./deploy.py [optional arguments]
```

The variable `PYTHON_EXECUTABLE` contains either the shortcut registered in your systems `$PATH` environment or the full direct path to the `python.exe`.


## What's inside?

### ./src/

Directory for all source files that will be synced to the brick.

Keep in mind, that many files slow down the process of copying, especially when relying on wireless connections to the remote EV3\. It is therefore recommended to keep only recent and relevant files in this folder.

### ./src/main.py

Central hub for the execution of any code.

The deploy script will call the function `main.run()`. Make sure that all modules are imported in this file and are called appropriately from within `run()`.

### ./deploy.py

Simple stub that calls the "real" `deploy.py` in the git submodule without an additional path prefix and passes along any parameters without modification.

This approach was chosen to allow updates in a very simple manner, without giving anyone headaches or create potential chaos due to merge conflicts and other similar entertaining problems. The process of updating is described in a section down below.

#### ./robolab-deploy/

Contains the "real" deploy module.

Including configuration files, scripts and necessary auxiliary binaries like `putty` and `pscp`. It is also the place for several other files, for instance login credentials, IP addresses and so on. These will not be added to any commit unless your override the .gitignore. For more information, please visit the [submodules repository](ttps://github.com/7HAL32/robolab-deploy).


## Updating

Hopefully updates are only necessary in order to get cool new features that have been added.
Well or in case any bug was found and had to be fixed, but that happens like, you know, never.
Luckily this process is fairly simple, as you make a pull in the submodule from the master and add the updated detached HEAD to a commit in the template repository.

```
$ git submodule foreach git pull origin master
$ git add robolab-deploy
$ git commit -m "* Updated submodule to lastest version of the upstream head"
$ git push
```


## Help

For additional information on usage, optional arguments, syntax, et cetera simply call the stub `deploy.py` with the `--help` flag.
There's also an extensive section on this template, the deploy scripts and the interface in the [RoboLab Docs](http://robolab.inf.tu-dresden.de) which are accessible via the campus network of TU Dresden.


## Credits

Contributors to robolab-template:

- [Frank Busse](https://github.com/251) (interface)
- Lutz Thies (description and deploy stub)
- Max Friedrich, Ian List, Kilian Koeltzsch and Sinthujan Thanabalasingam 

Contributors to [robolab-deploy](ttps://github.com/7HAL32/robolab-deploy) (submodule):

- Version of 2016

  - [Felix Döring](https://github.com/h4llow3En)
  - [Felix Wittwer](https://github.com/Feliix42)

- Version of 2017

  - [Paul Genssler](https://github.com/krabo0om) (systemd restart, debugging and testing for windows, emotional support)
  - Lutz Thies (rewrite and redesign, i.e. systemd, tmux, reloader)

Part of the RoboLab project.<br>
Released under the [MIT License](/LICENSE).<br>
Copyright © 2017-2018 Lutz Thies