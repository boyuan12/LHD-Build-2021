def smallest(arr):
    smallest_val = arr[0]
    index = 0
    for i in range(len(arr)):
        if arr[i] < smallest_val:
            smallest_val = arr[i]
            index = i
    return index


def check_finished(arr):
    for i in range(len(arr)):
        try:
            if arr[i+1] <= arr[i]:
                return False
        except IndexError:
            pass
    return True



def selection_sort(arr):
    smallest_index = smallest(arr)
    current_index = 0
    while not check_finished(arr):
        arr[current_index], arr[smallest_index] = arr[smallest_index], arr[current_index]
        current_index+=1
        print(arr)
    else:
        return arr


if __name__ == "__main__":
    lst = input("List: ")
    print(f"Sorted: {selection_sort(list(lst))}")

