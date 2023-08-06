outer_list = [1, 2, 3]

def delete_list(in_list: list) -> None:
    in_list = []

delete_list(outer_list)

print(outer_list)