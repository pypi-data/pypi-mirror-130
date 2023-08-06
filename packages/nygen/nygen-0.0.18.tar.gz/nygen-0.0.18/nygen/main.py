import argparse

from nygen.conf import init_conf
from nygen.lib.formatter import Formatter
from nygen.lib.gen import gen_project
from nygen.lib.exceptions import GenException


def parse_args() -> tuple[str, dict[str, str], dict[str, str]]:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    create_parser = subparsers.add_parser("create")
    create_parser.add_argument("name", help="Package name")
    create_parser.add_argument("--open", action="store_true", help="Open the project in vscode after creation")
    create_parser.add_argument("--open-dir", action="store_true", help="Open the project folder after creation")
    create_parser.add_argument("--template", action="store", help="Name of template to use", default="default")
    for arg_name, _var in Formatter.cmd_vars.items():
        create_parser.add_argument(f"--{arg_name}", help=_var.desc)

    init_parser = subparsers.add_parser("init")
    for arg_name, _var in Formatter.conf_vars.items():
        init_parser.add_argument(f"--{arg_name}", help="_var.desc")

    args = parser.parse_args()
    args_dict: dict[str, str] = vars(args)

    args.cmd_args = {arg_name: args_dict[arg_name] for arg_name in Formatter.cmd_vars if arg_name in args_dict}
    args.conf_args = {arg_name: args_dict[arg_name] for arg_name in Formatter.conf_vars if arg_name in args_dict}

    return args


def main():
    args = parse_args()

    if args.command == "init":
        print("Creating conf file")
        confpath = init_conf(args.conf_args)
        print(f"Created {confpath}")
    elif args.command == "create":
        try:
            gen_project(args.name, args.cmd_args, args.open, args.open_dir, args.template)
        except GenException as e:
            print(e)


if __name__ == "__main__":
    main()
