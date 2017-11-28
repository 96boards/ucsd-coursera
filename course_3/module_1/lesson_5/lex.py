import boto3

# Initialize lex client
client = boto3.client('lex-runtime')

print("Welcome to FlowerBot")

# Keep asking for questions until the conversation is done.
while(True):
    inputText = raw_input(
        "Send a message to FlowerBot [Enter 'q' to quit]: ")
    if(inputText == 'q'):
        break
        
    response = client.post_text(
        botName='OrderFlowers',     # Specify which bot
        botAlias='FlowerBot',       # Name of the version of the bot
        userId='person2',           # Tracks who the bot is talking to
        inputText= inputText        # User input
    )
    
    if(response['dialogState'] == 'ReadyForFulfillment'):
        print("Your flower order has been placed!")
        break
        
    # Show the user the Lex's response
    print(response['message'])
    
print("Thank you using FlowerBot! Have a nice day!")

