# Installing Flowblade 0.18 #

---

## Installing Debian Package ##

  * **Download .deb file** for Flowblade 0.18 from **[here](https://www.dropbox.com/s/v71v4e6y23dse2u/flowblade-0.18.0-1_all.deb?dl=0).**

  * Double Click on downloaded file to install.

**The download button may appear grayed out and you have to press it twice.**

**A window may appear that asks you to create an account but you can click a link at the bottom to download the file.**

**Please note: .deb file is in a Dropbox Public folder and may go over download limit, please contact Project Owner if this happens.**

### Supported OSes ###
  * This release has been tested on **Ubuntu 14.10**, **Ubuntu 14.04**, **Ubuntu 13.10**, **Linux Mint 17** and **Debian Testing (jessie/sid)**
  * May work on earlier Debian based systems

### Currently unsupported OSes ###
  * **Debian 7.2 or earlier**.  On these the application installed, but crashed on start-up, cause unknown. May work on some systems.


---


## Installing From Source Archive ##
  1. Donwload 0.18 source archive from [here](https://www.dropbox.com/s/qcw3gcyd6uioill/flowblade-0.18.0.tar.gz?dl=0).
  1. Extract archive into a folder of your choosing
  1. Install dependencies. See DependenciesList wiki for more information.
  1. Launch by running script **.../flowblade-0.18.0/flowblade** that was created in the folder where archive was unpacked
Flowblade is currently a 100% script application, and all the dependencies should be available in popular distributions, so in most cases it should be possible to install Flowblade without compiling anything.

**Please note: .tar.gz file is in a Dropbox Public folder and may go over download limit, please contact Project Owner if this happens.**


---


## Installing Developer Version ##

  1. Install Mercurial in your system.
  1. Use Mercurial to download Flowblade into a folder of your choosing by using the **hg clone** command in your terminal:
```
hg clone https://janne.liljeblad@code.google.com/p/flowblade/
```
  1. Install dependencies. See DependenciesList wiki for more information.
  1. Launch by running script **.../flowblade-trunk/flowblade** that was created in the folder where clone command was done.
Flowblade is currently a 100% script application, and all the dependencies should be available in popular distributions, so in most cases it should be possible to install Flowblade without compiling anything.

Developer version may however be unstable or have new dependencies. If you fail to install developer version, please file a bug in **Issues** -tab.

**NOTE: Using the available _setup.py_ script will NOT result in a successful installation, even if dependencies are installed, and may actually break the .deb install if attempted. It is only there to help .deb packaging.**


https://www.dropbox.com/s/9m2e9whcazjo1l8/flowblade-1.0.0-1_all.deb?dl=0