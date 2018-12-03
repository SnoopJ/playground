using DelimitedFiles

# read the data in without specifying the delimiter, but with an explicit type
# I don't think there's anyway to specify the type as a keyword argument to
# avoid positional headaches, but there are several signatures for this function
data = readdlm("input_day1.txt", Int)

# the answer to part 1 is just the sum of all the frequency shifts
freqshift = sum(data)

print("Frequency after one pass through the list: $freqshift\n\n")

# Part 2
# The built-in Iterators.cycle will let us
# loop over our data naturally

using Base.Iterators  # makes cycle() available without a prefix

function freqwalk(data)
    sum = 0
    seen = Set()  # Sets have O(1) membership testing
    for d in cycle(data)
        sum += d
        if sum in seen
            break
        else
            push!(seen, sum)  # Julia convention is ! with all functions that mutate
        end
    end
    return sum
end

finalfreq = freqwalk(data)

print("Calibration frequency (first repeated value): $finalfreq\n\n")
