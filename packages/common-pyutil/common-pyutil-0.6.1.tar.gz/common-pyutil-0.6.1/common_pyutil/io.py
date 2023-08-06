def prompt(string, p_t, p_f):
    x = input(string).strip()
    if isinstance(p_t, str):
        p_t = {p_t}
    if isinstance(p_f, str):
        p_f = {p_f}
    valid_inputs = {*p_t, *p_f}
    while x not in valid_inputs:
        x = input(string + f"\nPlease type one of {valid_inputs} ").strip()
    if x in p_t:
        return True
    elif x in p_f:
        return False


def prompt_yes_no(string):
    return prompt(string + " (yes or no) ", "yes", "no")


def prompt_y_n(string):
    return prompt(string + " (y, n) ", {"yes", "y"}, {"no", "n"})
