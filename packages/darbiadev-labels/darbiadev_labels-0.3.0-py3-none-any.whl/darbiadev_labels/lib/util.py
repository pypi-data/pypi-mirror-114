#!/usr/bin/env python


def prefix_separator_zfilled_number(
        prefix: str,
        separator: str = '-',
        start: int = 1,
        end: int = 1,
        zeroes: int = 3
):
    return [prefix + separator + str(i).zfill(zeroes) for i in range(start, end + 1)]
