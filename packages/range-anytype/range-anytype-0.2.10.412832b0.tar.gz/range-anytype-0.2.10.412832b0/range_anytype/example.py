#!/usr/bin/env python3
# coding=UTF-8

def restart() :
    print("EXAMPLE START: range_anytype")
    for i in [
    "from range_anytype import Range, ProtectedRange",
    "print(Range(9))",
    "print(ProtectedRange(12))",
    "import decimal, fractions",
    "print(Range(9, 32, 0.4))",
    "print(Range(decimal.Decimal(9), decimal.Decimal(32), decimal.Decimal('0.4')))",
    "print(Range(fractions.Fraction(9), fractions.Fraction(32), fractions.Fraction(2, 5)))",
    """\
for i in Range(-fractions.Fraction(256, 24), fractions.Fraction(512, 17), fractions.Fraction(1, 18)) :
    print(i)""",
    "print(tuple(Range(-fractions.Fraction(256, 24), fractions.Fraction(512, 17), fractions.Fraction(1, 18))))"
    ] :
        print(">>> "+"\n... ".join(i.split("\n")))
        exec("global Range, ProtectedRange, decimal, fractions\n"+i)

restart()
