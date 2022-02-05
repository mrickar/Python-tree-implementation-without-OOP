def find_root(part_list):
    for t in part_list:
        chc = 1
        for i in part_list:
            for j in i:
                # is the part exist as child of another part
                if type(j) == tuple and t[0] == j[1]:
                    chc = 0
                    break
            if chc == 0:
                break
        if chc == 1:  # if not child of another part return it
            return t[0]  # name of the root returns


def tree_build(part_list, name):
    for i in part_list:
        if i[0] == name:
            ln = len(i)
            for j in range(ln):
                if type(i[j]) == tuple:
                    # (number,name) changes to [number + itself and childs]
                    i[j] = [i[j][0]] + tree_build(part_list, i[j][1])
            return i  # after all tuples are converted return it


def make_tree(part_list):
    temp_list = []
    for i in part_list:  # copying elemants of list to another list
        temp_list.append(i[:])

    root = find_root(temp_list)  # finds the root of the tree
    tree_build(temp_list, root)  # makes tree
    for i in temp_list:
        if i[0] == root:  # the elemant that starts with the root is assign to "tree"
            tree = i
            break

    return [1]+tree  # number of the first elemant [1] and the tree returns


def calculate_price(part_list):
    tree = make_tree(part_list)

    def solve_calcP(amount, tree):
        price = 0
        if type(tree[2]) != list:  # if doesnt have childs
            return amount*(tree[2])  # return needed amount*price
        for i in tree:
            if type(i) == list:  # if it is a child
                price += solve_calcP(amount*(i[0]), i)
        return price
    price = solve_calcP(1, tree)
    return price


def required_parts(part_list):
    # return list of tuples -> (total_quantity,basic_part)
    tree = make_tree(part_list)
    global rp
    rp = []

    def solve_reqP(amount, tree):
        global rp
        if type(tree[2]) != list:  # if doesnt have childs
            tp = (amount, tree[1])
            rp.append(tp)  # add amount,name
            return
        for i in tree:
            if type(i) == list:  # if it is a child
                solve_reqP(amount*(i[0]), i)
    solve_reqP(1, tree)
    return rp


def stock_check(part_list, stock_list):
    # stock list -> list of tuples (stock_quantity,basic_part)
    # func. computes the shorts in stock -> (N-M) N:need M:provided
    # returns shorts   (basic_part,shortness_amount)
    need = []
    req = required_parts(part_list)
    for i in req:
        check = 0
        for j in stock_list:
            if i[1] == j[1]:  # if part exists in stock_list
                check = 1
                if i[0] > j[0]:  # if it is not enough
                    need.append((i[1], i[0]-j[0]))
                break
        if check == 0:  # if that part not exist in stock_list
            need.append((i[1], i[0]))
    return need
