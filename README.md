# nicehash-on-linux
Simple python script to mine using GPU(gminer)/CPU(xmrig) on linux (nicehash)

Run as Sudo if you wish to use xmrig`s msr mod

Tested on arch linux. Install gminer and xmrig on your system manually if it is not arch.

Edit config.ini after first start to change options.

To allow Gpu Fan Control set coolbits to 31
sudo nvidia-xconfig -a --cool-bits=31 --allow-empty-initial-configuration
