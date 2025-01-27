def is_valid_password(new_pass):
    count1 = count2 = count3 = count4 = 0
    for i in new_pass:
        if "0" < i < "9":
            count1 = 1
        if "A" < i < "Z":
            count2 = 1
        if "a" < i < "z":
            count3 = 1
        # if "!" < i < "(":
        #     count4 = 1
    if count1 == 1 and count2 == 1 and count3 == 1:
        return True
    return False
