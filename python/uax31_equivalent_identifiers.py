# Python implements UAX #31, so we can use non-ASCII identifiers
# for more information, see:
#
# https://docs.python.org/3/reference/lexical_analysis.html#identifiers
# https://peps.python.org/pep-3131/
# https://unicode.org/reports/tr31

パイソン = "\N{SNAKE}"
print(f"{パイソン = }")

# UAX #31 also specifies rules for what identifiers should be considered
# equivalent to each other, and Python respects these rules, so we can
# refer to the name we just defined using the half-width kana form
# More specifically, these forms of the kana spelling of "Python" are
# equivalent under the NFKC normalization form
# https://unicode.org/reports/tr31/#normalization_and_case

print(f"{ﾊﾟｲｿﾝ = }")
