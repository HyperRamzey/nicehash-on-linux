# nicehash-on-linux
Simple python script to mine using GPU(miniZ)/CPU(xmrig) on linux (or windows), on nicehash pools.

Tested on arch linux and Win10. Install curl and p7zip on your system manually if it is not arch. Install 7z on windows.

Edit config.ini after first start to change options.

To allow nvidia Gpu Fan Control in linux set coolbits to 31 

sudo nvidia-xconfig -a --cool-bits=31 --allow-empty-initial-configuration


# roadmap
~~add multi gpu support for fan control~~ Added in 1.2 as miniz command

~~add locking clock, undervolt, pl limits~~ Added in 1.3.0

~~add different algos~~ Added in 1.2

~~add support for other distros~~ Kinda added in 1.2
