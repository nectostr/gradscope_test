def bubble_sort(nums):
    resulting_list = nums.copy()
    for _ in range(len(resulting_list) - 1):
        changes = False
        for i in range(len(resulting_list)-1):
            if resulting_list[i] < resulting_list[i+1]:
                print(f"Making exchange {resulting_list[i]} on {resulting_list[i + 1]}")
                resulting_list[i], resulting_list[i + 1] = resulting_list[i + 1], resulting_list[i]
                changes = True
        if not changes:
            break
    return resulting_list
