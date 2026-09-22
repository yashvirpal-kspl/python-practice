def chai_flavor(flavor="masala"):
    """Return the flavor of the chai"""  #it's work only if write in first line of function
    return flavor
print(chai_flavor)
print(chai_flavor.__doc__)    # __ called dunder
print(chai_flavor.__name__)


help(len)


def generate_bill(chai=0,samosa=0):
    """
    Calculate the total bill for chai and samosa
    
    :param chai: Number of chai cups(10 rupes each)
    :param samosa: Number of Samosa (15 rupes each)
    :return : (total amount , thankyou message)
    """
    total=chai*10+samosa*15
    return total,"Thankyou for visiting yashvirpal.com"
print(generate_bill(2,4)) 

help(generate_bill)
