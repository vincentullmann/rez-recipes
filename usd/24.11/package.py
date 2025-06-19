name = "usd"
version = "24.11"

requires = [
    "~ptex-2.0+",
    "boost-1.70+",
    "glew-2.1",
    "jinja2",
    "numpy",
    "ocio-2.4",
    "oiio-2",
    "openexr-3",
    "osd-3.4+",
    "pyopengl-3.1",
    "pyside6-6.5",
    "python",
    "tbb-2020+",
]


hashed_variants = True

@early()
def build_requires():
    import platform

    if platform.system() == "Windows":
        return ["cmake", "vs"]
    else:
        return ["cmake"]


@early()
def variants():
    import os, ast

    cook_variant = os.getenv("REZ_COOK_VARIANT")
    if cook_variant:
        # If we're building the package, we want to use the variant supplied to us
        return [ast.literal_eval(cook_variant)]
    # else:
    # Otherwise tell rez-cook what variants we are capable of building

    return [
        ["platform-linux"],
        # ["platform-windows", "arch-AMD64", "vs"],
    ]


def commands():
    env.USD_ROOT = "{root}"
    env.CMAKE_PREFIX_PATH.prepend("{root}")
    env.PATH.prepend("{root}/bin")
    env.PATH.prepend("{root}/lib")
    env.PYTHONPATH.prepend("{root}/lib/python")

    import platform

    if platform.system() == "Linux":
        env.LD_LIBRARY_PATH.prepend("{root}/lib")
        env.PYOPENGL_PLATFORM = "glx"


def env(var: str):
    import platform

    if platform.system() == "Windows":
        return f"$env:{var}"
    else:
        return f"${var}"


config_args = [
    "cmake",
    "{root}",
    "-DCMAKE_INSTALL_PREFIX={install_path}",
    f'-DCMAKE_MODULE_PATH="{env("CMAKE_MODULE_PATH")}"',
    f'-DCMAKE_BUILD_TYPE="{env("REZ_BUILD_CONFIG")}"',
    f'-DTBB_LOCATION="{env("TBB_LOCATION")}"',
    f'-DOPENEXR_LOCATION="{env("OPENEXR_ROOT")}"',
    f'-DOPENSUBDIV_ROOT_DIR="{env("OPENSUBDIV_ROOT")}"',
    f'-DPTEX_LOCATION="{env("Ptex_ROOT")}"',
    f'-DOIIO_LOCATION="{env("OpenImageIO_ROOT")}"',
    f'-DBOOST_ROOT="{env("Boost_ROOT")}"',

    f'-DPython_ROOT="{env("Python_ROOT")}"',
    f'-DPython3_ROOT="{env("Python_ROOT")}"',
    f'-DPython_EXECUTABLE="{env("Python_EXECUTABLE")}"',
    f'-DPython3_EXECUTABLE="{env("Python_EXECUTABLE")}"',

    # f'-DPython_ROOT="{env("Python_ROOT")}"',
    # f'-DPython3_ROOT="{env("Python_ROOT")}"',

    # '-DPython_EXECUTABLE=/usr/bin/python3.11',
    # '-DPython3_EXECUTABLE=/usr/bin/python3.11',
    # '-DPYTHON_LIBRARY=/usr/lib/x86_64-linux-gnu/libpython3.11.so',
    # "-DPYTHON_INCLUDE_DIR=/usr/include/python3.11",


    "-DPXR_BUILD_DOCUMENTATION=FALSE",
    "-DPXR_BUILD_TESTS=FALSE",
    "-DPXR_BUILD_EXAMPLES=FALSE",
    "-DPXR_USE_PYTHON_3=ON",
    "-DCMAKE_CXX_STANDARD=17",
    # Fix for boost inserting the wrong library names into the libs with 
    # --layout=system...
    # f'-DCMAKE_CXX_FLAGS="-DBOOST_ALL_NO_LIB -D__TBB_show_deprecation_message_task_H -DBOOST_BIND_GLOBAL_PLACEHOLDERS -Wno-class-memaccess {env("CXXFLAGS")}"',
    # " -G Ninja",
]

import platform

if platform.system() == "Linux":
    config_args.append(f'-DCMAKE_CXX_FLAGS="-DBOOST_ALL_NO_LIB -D__TBB_show_deprecation_message_task_H -DBOOST_BIND_GLOBAL_PLACEHOLDERS -Wno-class-memaccess {env("CXXFLAGS")}"')
else:
    config_args.append(f'-DCMAKE_CXX_FLAGS="-DBOOST_ALL_NO_LIB -D__TBB_show_deprecation_message_task_H -DBOOST_BIND_GLOBAL_PLACEHOLDERS {env("CXXFLAGS")}"')


build_command = (
    " ".join(config_args)
    + f" && cmake --build . --target install --config {env('REZ_BUILD_CONFIG')}"
)


def pre_cook():
    download_and_unpack(
        f"https://github.com/PixarAnimationStudios/USD/archive/refs/tags/v{version}.tar.gz"
    )
