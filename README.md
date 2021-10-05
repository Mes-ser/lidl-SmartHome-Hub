# Lidl Smart Home HUB RE
_My journey with Lidl smart home hub_

## But why?

- For fun
- Discovering how it works
- Trying new tools
- Understanding how Linux boot and works
- And a lot more

## Current progress

- Extracted Bootloader, Kernel+Conf, file system, device specific data (Label)
- Backup and recover bricked HUB (Learned this the hard way)
- There's ssh running (`dropbear`) which requires ssh key to login
- How to edit file system and pack it again

## Tools
- Python (didn't expected that huh? :) )
- `Binwalk` with `jefferson`, `unsquashfs` (and other - don't remember but installed them all) plugins
- `Flashrom`
- CH341A Mini Programmer or other tool to read/write SPI flash memory
- debug probe for SPI chip
- Soldering iron
- Some tools to open case ex. old phone/credit card (Its hard - trust me)
- Time

## Platform

This smart hub is based on Tuya white label using their own Zigbee module TYZS4, RTL8196E-CG ethernet router network processor, GD25Q127C SPI 128Mbit Flash memory to store Linux image, EM6AA160 DRAM.

## Extracting image

Connect debug probe to SPI flash and run:
```sh
flashrom --programmer ch341a_spi -c GD25Q127C/GD25Q128C -r gw_backup.bin
```

Now you can use Binwalk to see what’s inside this image, but for me it didn't work.
`binwalk` was discovering a lot of zlib file headers and automatic extraction was absolute mess - After a lot of try and error I flashed dumped image (Don't know why...) and bricked my HUB (Maybe somewhere I changed something)

>In meantime learned that binwalk has some issues when matching file headers

Long story short - Purchased second HUB and started again but this time I was more careful.

After dumping new image I used `extract.py` to extract individual images which gave me:
- boot+cfg offset=0x0 size=0x20000 erasesize=0x10000
Assumed bootloader and config for realtek chip.
- linux offset=0x20000 size=0x1e0000 erasesize=0x10000
Linux kernel
- rootfs offset=0x200000 size=0x200000 erasesize=0x10000
Linux file systsem
- tuya-label offset=0x400000 size=0x20000 erasesize=0x10000
- jffs2-fs offset=0x420000 size=0xbe0000 erasesize=0x10000

Then using `jefferson` for jffs2-fs and `unsquashfs` for rootfs successfully acquired access to files and file system.

### rootfs
### jffs2-fs

## TBC...
