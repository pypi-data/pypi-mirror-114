# kdump
Static Mach-O binary metadata analysis tool / information dumper
---

### Installation

```shell
pip3 install kdump
```

### Usage

```shell
usage: kdump [-h] [--map] [--classes] [--binding] [--class GETCLASS] [--headers] [--out OUTDIR] filename

```

`--headers` Dumps headers to directory specified by `--out`  
`--out <directory>` Directory to dump headers for class  
`--map` Prints a map of segments/sections, and their respective VM/File offsets  
`--classes` Dumps classnames  
`--binding` Prints binding info actions  
`--class` Get info about a specific class  

---

written in python for the sake of platform independence when operating on static binaries and libraries

#### Special thanks to

IDA for making it possible to write the code without actually understanding full internals  
JLevin and *OS Internals Vol 1 for actually understanding the internals and specifics + writing documentation  
arandomdev for guidance + code