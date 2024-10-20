def permute(s, answer):
    # Base case: if the string is empty, print the accumulated answer
    if len(s) == 0:
        print(answer)
        return
    # Recursive case: iterate through the string
    for i in range(len(s)):
        # Choose the current character and append it to the answer
        char = s[i]
        # Remaining string after removing the chosen character
        remaining = s[:i] + s[i + 1:]
        # Recursive call with the remaining string and updated answer
        permute(remaining, answer + char)


# Driver code
string = "abc"
# Call the permute function
permute(string, "")


s = 'abcde'

permutations = s[0]

for i in range(1,len(s)):
    char = s[i]
    # print(f'inum: {i}, char = {char}')
    ## permutaions
    temp_perms = []
    for perm in permutations:
        # print(f'inum: {i}, perm = {perm}')

        for j in range(len(perm)+1):
            # print(f'inum: {i}')
            # print(f'perm: {perm}')
            # print(f'front: {perm[:j]}, j={j}')
            # print(f'char: {char}')
            # print(f'rest: {perm[j:]}, j={j}')
            temp_perms.append(perm[:j] + char + perm[j:]) #j= 0 => ba, j=1
            # print(f'all: {front}\n')
        # print(f'END OF FILE')
    permutations = temp_perms
print(permutations)
print(len(permutations))


def get_permutations(string, perm_length):
    def permute(prefix, remaining):
        if len(prefix) == perm_length:
            permutations_list.append(prefix)
            return
        for i in range(len(remaining)):
            permute(prefix + remaining[i], remaining[:i] + remaining[i + 1:])

    permutations_list = []
    permute("", string)
    return permutations_list


string = 'abcd'
perm_length = 3  # Set your permutation length dynamically here
permutations = get_permutations(string, perm_length)
print(permutations)



