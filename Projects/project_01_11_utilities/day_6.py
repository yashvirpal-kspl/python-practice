import datetime

entry=input("What did you learn today ? ").strip()
rating=input("⭐ rate your productvity today (1-5,optional) ").strip()


now =datetime.datetime.now()
date_str=now.strftime("%Y-%m-%d  -  %I:%M %p")

journal_entry=f"\n📅 {date_str}\n{entry}"
if rating:
    journal_entry += f"\nProductvity Rating: {rating}\n"
    
with open("learnal_journal.txt","a",encoding="utf-8") as f :
    f.write(journal_entry)
    
print(f"\n your journal enatry has been saved to 'learning_journal.txt' file. ")        