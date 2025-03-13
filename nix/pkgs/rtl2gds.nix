{
  lib,
  bash,
  ieda,
  yosys,
  klayout-pypi,
  buildPythonPackage,
  python3,
  python3Packages,
}:
buildPythonPackage {
  pname = "rtl2gds";
  version = "0.1.0";
  pyproject = true;
  src = ./../..;

  propagatedBuildInputs =
    with python3Packages;
    [
      python3
      setuptools

      pyyaml
      orjson
      klayout-pypi
      hatchling
      requests
    ]
    ++ [
      ieda
      yosys
    ];

  nativeBuildInputs = with python3Packages; [
    setuptools
    wheel
  ];
  doCheck = false;

  makeWrapperArgs = [
    "--set PATH ${
      lib.makeBinPath [
        bash
        yosys
        ieda
      ]
    }"
    "--set LD_LIBRARY_PATH ${
      lib.makeLibraryPath [
        python3Packages.pyyaml
        python3Packages.orjson
        klayout-pypi
      ]
    }"
  ];

  meta = {
    description = "A tool to compile your RTL files into GDSII layouts.";
    homepage = "https://github.com/0xharry/RTL2GDS";
  };
}
