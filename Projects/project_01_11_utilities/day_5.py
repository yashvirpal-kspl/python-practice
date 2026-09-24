
#get a dictionary
emoji_mao_fun={
    "love":"💚",
    "happy":"😄",
    "code":"💻",
    "tea":"☕",
    "music":"🎵",
    "food":"🍲",
}


#get user message
message=input("Enter your message: ")

updated_words=[]
#process each word
for word in message.split():
    cleaned=word.lower().strip(".,!?")
    emoji = emoji_mao_fun.get(cleaned,"")
    if emoji:
        updated_words.append(f"{word} {emoji}")
    else:
        updated_words.append(word)    
        
#Array to String Convert
updated_message=" ".join(updated_words)  
print("\nEnhanced message\n")
print(updated_message)      