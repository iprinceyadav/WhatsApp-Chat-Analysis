import re
import pandas as pd


def preprocess(data):
    pattern=r'\d{1,2}\/\d{1,2}\/\d{2},\s\d{1,2}:\d{2}\s(?:am|pm)'
    message = re.split(pattern,data)[1:]
    dates=re.findall(pattern,data)
    df = pd.DataFrame({'user_message': message, 'message_date': dates})
    # convert message_date type
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %I:%M %p')


    df.rename(columns={'message_date': 'date'}, inplace=True)
    users = []
    messages = []  # Renamed to avoid conflict with the loop variable

# Assuming 'user_message' is your column with user and message data
    for entry in df['user_message']:
    # Adjusting the split pattern to match the format more accurately
        result = re.split(r'(\S+):\s', entry)  # Assuming format 'User: Message'
    
        if len(result) > 1:
            users.append(result[1])  # The user name is at position 1
            messages.append(result[2])  # The message content is at position 2
        else:
            users.append('group_notification')  # For group notifications (if applicable)
            messages.append(result[0])  # In case of no user info, just append the message

    # Add new columns
    df['user'] = users
    df['message'] = messages

    # Drop the original 'user_message' column
    df.drop(columns=['user_message'], inplace=True)
    df['year']=df['date'].dt.year
    df['month']=df['date'].dt.month_name()
    df['day']=df['date'].dt.day
    df['hour']=df['date'].dt.hour
    df['minute']=df['date'].dt.minute

    return df