import re  # Module for pattern matching

#Read the file
arr = []
with open("problemLinks.txt", "r") as file:
    for line in file:
        arr.append(line)


#   Function to remove elements the elements with a specified pattern
def filter_problem_titles(array, pattern):
    new_array = []
    for element in array:
        if pattern not in element:
            new_array.append(element)
        else:
            print("Removed: " + element)
    return new_array

#   We want to remove the elements with the following pattern
# arr[108].href
# 'https://leetcode.com/problems/add-two-numbers/'
# arr[109].href
# 'https://leetcode.com/problems/add-two-numbers/solution'
arr = filter_problem_titles(arr, "/solution")
print(len(arr))
arr = list(set(arr))

with open('FilteredProblemLinks.txt', 'a') as f:
    for j in arr:
        f.write(j)
