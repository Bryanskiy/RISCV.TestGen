import argparse
import yaml
from pathlib import Path
import subprocess

import isa.info


def main() -> None:
    """Main function"""

    parser = argparse.ArgumentParser(description="Tool to RISCV tests")

    parser.add_argument(
        "-c", "--config", required=True, type=Path, help="configuration file"
    )

    args = parser.parse_args()

    with open(args.config, encoding="utf-8") as yml:
        yaml_data = yaml.safe_load(yml)

    script = Path(yaml_data["riscv_script"])

    extensions = list(map(str, yaml_data["test_opts"]["extensions"]))

    try:
        status = subprocess.run(
            ["python3", script.resolve(), *extensions],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            cwd=script.parent,
        )
        print(str(status.stdout, "utf-8"))
    except subprocess.CalledProcessError as ex:
        print(
            f"Command {' '.join(map(str, ex.cmd))} exited w/ non zero status: {ex.stdout}"
        )

    with open(script.with_name("instr_dict.yaml"), encoding="utf-8") as yml:
        inst_data = yaml.safe_load(yml)

    isa.info.generate_enums(inst_data)

    for name, fmt in isa.info.NAME_TO_FORMAT.items():
        if fmt in (isa.info.InstrFormatTy.I,):
            print(name)


if "__main__" == __name__:
    main()
