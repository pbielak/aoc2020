"""Day 4 - Advent of Code"""
from typing import Dict, List


def parse_file(path: str) -> List[Dict[str, str]]:
    passports = []

    record = ''
    with open(path, 'r') as fin:
        for row in fin.readlines():
            row = row.replace('\n', ' ')

            if row == ' ':
                passports.append({
                    v.split(':')[0]: v.split(':')[1]
                    for v in record.strip().split(' ')
                })
                record = ''
            else:
                record += row

        passports.append({
            v.split(':')[0]: v.split(':')[1]
            for v in record.strip().split(' ')
        })

    return passports


def has_all_required_keys(
    passport: Dict[str, str],
    required_fields: List[str] = (
        'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid',
    ),
) -> bool:
    return all(rf in passport.keys() for rf in required_fields)


def is_valid_passport(
    passport: Dict[str, str],
) -> bool:
    # Validate `Birth Year`
    byr = passport['byr']
    if not (len(byr) == 4 and (1920 <= int(byr) <= 2002)):
        return False

    # Validate `Issue Year`
    iyr = passport['iyr']
    if not (len(iyr) == 4 and (2010 <= int(iyr) <= 2020)):
        return False

    # Validate `Expiration Year`
    eyr = passport['eyr']
    if not (len(eyr) == 4 and (2020 <= int(eyr) <= 2030)):
        return False

    # Validate `Height`
    hgt = passport['hgt']
    if not (
        ('cm' in hgt or 'in' in hgt)
        and (
            (('cm' in hgt) and (150 <= int(hgt.split('cm')[0]) <= 193))
            or (('in' in hgt) and (59 <= int(hgt.split('in')[0]) <= 76))
        )
    ):
        return False

    # Validate `Hair Color`
    hcl = passport['hcl']
    if not(
        len(hcl) == 7
        and hcl.startswith('#')
        and all(
            ('0' <= c <= '9') or ('a' <= c <= 'f')
            for c in hcl[1:]
        )
    ):
        return False

    # Validate `Eye Color'
    ecl = passport['ecl']
    if not any(
        ecl == v
        for v in ('amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth')
    ):
        return False

    # Validate `Passport ID`
    pid = passport['pid']
    if not (
        len(pid) == 9
        and any('0' <= c <= '9' for c in pid)
    ):
        return False

    return True


def main():
    test_files = ['./data/example.txt', './data/input.txt']

    for tf in test_files:
        print('Test file:', tf)

        passport_data = parse_file(path=tf)

        num_valid = len([
            passport
            for passport in passport_data
            if has_all_required_keys(passport=passport)
        ])
        print('(Part 1) Number of valid passports:', num_valid)

        num_valid = len([
            passport
            for passport in passport_data
            if (
                has_all_required_keys(passport=passport)
                and is_valid_passport(passport=passport)
            )
        ])
        print('(Part 2) Number of valid passports:', num_valid)

        print('-------')


if __name__ == '__main__':
    main()
