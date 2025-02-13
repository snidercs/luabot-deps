# LuaBOT - WPILib
This project contains utilities that assemble official wpilib libraries and headers needed to target the roborio.  These artifacts, after running `install.sh`, get placed in the same base path to an installed WPIlib. e.g. Artifiacts go here: `$HOME/wpilib/2025/luabot/**/*`

**Experimental**: if using this project as a meson subproject, then running the install script is not necessary.

**LuaJIT**: As an aside, this project also builds lua jit targeting the rio. TODO: move to it's own project.
ds

## Install It
```
meson setup build
ninja -C build
sh install.sh
```

## Cmake and Meson Toolchains
WPILib provides the toolchain config file `~/wpilib/2025/roborio/toolchain-config.cmake` for CMake.  If `meson-cross.ini` and `meson-native.ini` are copied to the same location, they then be by with Meson's `--cross-file` and `--native-file` to easily cross compile code for the RIO.  

**Note**: The *native* file is only needed when compiling projects require the build machine is in 32 bit mode.