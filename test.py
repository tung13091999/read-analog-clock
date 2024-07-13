def split_list_approximate(lst, threshold):
    sub_lists = []
    current_sublist = [lst[0]]

    for i in range(1, len(lst)):
        if abs(lst[i-1] - lst[i]) <= threshold:
            current_sublist.append(lst[i])
        else:
            sub_lists.append(current_sublist)
            current_sublist = [lst[i]]
    sub_lists.append(current_sublist)
    return sub_lists


my_list = [1.1, 1.2, 1.3, 2.0, 2.1, 2.2, 3.0, 3.1]
threshold = 0.2

sub_lists = split_list_approximate(my_list, threshold)
print(sub_lists)
