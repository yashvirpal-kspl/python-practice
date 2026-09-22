# def make_chai():
#     return "Here is your msala chai"

# response=make_chai()
# print(response)

# Return None type
def idle_chaiwala():
    pass

print(idle_chaiwala())


# return one value type
def sold_cups():
    return 10

sldcps=sold_cups()
print(sldcps)


# Early return type  
def chai_status(cup_left):
    if cup_left==0:
        return "Sorry, chai over"
    return "Chai is ready"

#sts=chai_status(0)
sts=chai_status(6)
print(sts)

# Multiple return Type
def chai_report():
    return 10,200

sold,remaining=chai_report()
print("Sold",sold)
print("Remaining",remaining)
