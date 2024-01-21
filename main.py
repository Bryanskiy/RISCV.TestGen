import argparse
import yaml
import generator as gen
from pathlib import Path

def main() -> None:
    """Main function"""

    parser = argparse.ArgumentParser(
        description="Tool to RISCV tests"
    )

    parser.add_argument(
        "-c", "--config", required=True, type=Path, help="configuration file"
    )

    args = parser.parse_args()

    with open(args.config, encoding="utf-8") as yml:
        yaml_data = yaml.safe_load(yml)

    generator = gen.Generator()
    instrs = generator.generate()
    for instr in instrs: print(instr.into_asm())

if "__main__" == __name__:
    main()
