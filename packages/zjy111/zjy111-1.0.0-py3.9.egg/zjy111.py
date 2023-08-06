"""
This is a modle for print a list.
"""

def print_lol(the_list):
    
    """
    The function of print_lol is a test function.
    """
    for term in the_list:
        if(isinstance(term,list)):
            print_lol(term)
        else:
            print(term)
