users=[
    {"id":1,"total":100,"coupon":"W20"},
    {"id":2,"total":150,"coupon":"T50"},
    {"id":3,"total":80,"coupon":"S30"},
    {"id":4,"total":500,"coupon":"F10"},
]
discounts={
    "W20":(0.2,0),
    "T50":(0.5,0),
    "S30":(0.3,0), # percent discount
    "F10":(0,10),  # Flat discount 
}
for user in users:
    #percent,fixed=discounts.get('coupon')
    percent,fixed=discounts.get(user['coupon'],(0,0))
    discount=user['total'] * percent + fixed
    print(f"{user['id']} paid {user['total']} and got for next visit of rupees {discount}")