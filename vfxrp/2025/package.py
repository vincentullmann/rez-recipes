name = "vfxrp"
version = "2025"

@early()
def requires():
    req = [
        "~python-3.11",
        "~pyqt6-6.5",
        "~pyside6-6.5",
        "~numpy-1.26",
        "~openexr-3.3",
        "~ptex-2.4",
        "~osd-3.6",
        "~openvdb-12",
        "~alembic-1.8",
        "~ocio-2.4",
        "~boost-1.85",
        "~tbb-2021",
    ]

    import platform
    if platform.system() == "Windows":
        req += ["vs-2022"]
    else:
        req += ["cxx11abi-1"]

    return req


@early()
def variants():
    import os, ast

    cook_variant = os.getenv("REZ_COOK_VARIANT")
    if cook_variant:
        # If we're building the package, we want to use the variant supplied to us
        return [ast.literal_eval(cook_variant)]
    else:
        # Otherwise tell rez-cook what variants we are capable of building
        return [
            ["platform-linux", "arch-x86_64", "cfg"],
            ["platform-windows", "arch-AMD64", "cfg"],
        ]
