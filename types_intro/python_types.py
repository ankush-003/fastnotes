def add(firstname, lastname):
    return firstname + " " + lastname

def addTypes(firstname: str, lastname: str) -> str:
    return firstname + " " + lastname
fname = "Ankush"
lname = "H V"

def numList(nums: list[int], num2: list[int, int] | None = None) -> None:
    for num in nums:
        print(num, end=" ")
    print(type(num2))
    if num2 is not None:
        print(num2[0], num2[1])

# we can get propmts for variables
name = add(fname, lname)
print(name)
name2 = addTypes(fname, lname)
print(f"Hello {name2}")
numList([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
numList([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [1, 2])