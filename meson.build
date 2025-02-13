project ('luabot-wpilib', ['cpp', 'c'], 
    version : '2025.2.1',
    meson_version : '>= 1.4.0',
    license : 'MIT',
    default_options: [
        'b_ndebug=if-release',
        'buildtype=release',
        'cpp_std=c++20',
    ])

# Python
pymod = import ('python')
python_exe = pymod.find_installation ('python3', 
    modules : [])

# Dependency builder.
riodeps_py = files ('riodeps.py')
prebuilts_dep = custom_target ('riodeps',
    build_by_default: true,
    command: [ python_exe, riodeps_py ],
    output : 'riodeps.stamp',
    capture: true,
    install: false)
