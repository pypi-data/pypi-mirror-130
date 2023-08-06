import typer
from typing import List
from stdin_processor.processor import STDIN, backslashed, parse_index_pattern
from stdin_processor import global_args
import re
import sys

def _replace(*old, new, string, **kwargs):
    position_pattern = kwargs.get('position_pattern', None)
    ignore_case = kwargs.get('ignore_case', False)
    s = string
    replacement = backslashed(new)

    for regex in old:
        if position_pattern:
            matches = re.finditer(regex, s, re.IGNORECASE) if ignore_case else re.finditer(regex, s)
            positions_in_string = list(map(lambda m: m.span(), matches))
            target_indexes = parse_index_pattern(positions_in_string, position_pattern)
            s = list(s)
            for i in reversed(range(len(positions_in_string))):
                if i in target_indexes:
                    start = positions_in_string[i][0]
                    end = positions_in_string[i][1]
                    s[start:end] = list(replacement)
            s = ''.join(s)

        # think to check if working when new longer than old or opposite

        else:
            if ignore_case:
                matches = re.compile(regex, re.IGNORECASE)
            else:
                matches = re.compile(regex)
            s = matches.sub(replacement, s)

    return s


def replace(replacement: str = typer.Argument(''),
            targets: List[str] = typer.Option(None, '--regex', '-e', help='Regular expressions to replace followed by the replacement [ex:  \'1 2 3 0\'  to replace 1, 2 and 3 by 0]'),
            position: str = typer.Option(None, '--position', '-p', help='Comma separated list of positions corresponding to the list of matches [ex: :2,4,6:]'),
            replace_ignore_case: bool = typer.Option(False, '--ic', '--rI', help='Ignore case for strings to replace, do not confuse with -I which is used with --where'),
            ____________________________: str = global_args.args_separator,
            separators: List[str] = global_args.separators,
            group_by: int = global_args.group_by,
            join: str = global_args.join,
            unique: bool = global_args.unique,
            sort: str = global_args.sort,
            sort_key: str = global_args.sort_key,
            shuffle: bool = global_args.shuffle,
            keep: bool = global_args.keep,
            where: List[str] = global_args.where,
            start_where: str = global_args.start_where,
            stop_where: str = global_args.stop_where,
            indexes: str = global_args.index,
            _not: bool = global_args._not,
            rotation: int = global_args.rotation,
            reverse: bool = global_args.reverse,
            ignore_case: bool = global_args.ignore_case
            ):

    stdin = STDIN(sys.stdin.read())
    stdin.process(lambda x: _replace(*targets,
                                     new=replacement,
                                     string=x,
                                     position_pattern=position,
                                     ignore_case=replace_ignore_case),
                  separators=separators,
                  group_by=group_by,
                  unique=unique,
                  sort=sort,
                  sort_key=sort_key,
                  shuffle=shuffle,
                  keep=keep,
                  where=where,
                  start_where=start_where,
                  stop_where=stop_where,
                  _not=_not,
                  ignore_case=ignore_case,
                  indexes=indexes,
                  rotation=rotation,
                  reverse=reverse,
                  joiner=join)

    print(stdin.value, end='' if stdin.value.endswith('\n') else '\n')
