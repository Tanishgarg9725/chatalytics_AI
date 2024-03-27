import re
import pandas as pd
def preprocess(data):
    pattern = '\d{2}/\d{2}/\d{4},\s\d{2}:\d{2}\s(?:am|pm)\s-\s'

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    # Convert dates to datetime objects
    date_times = pd.to_datetime(dates, format='%d/%m/%Y, %I:%M %p - ')

    # Create DataFrame with messages and datetime objects
    df = pd.DataFrame({'user_message': messages, 'message_date': date_times})

    # Rename the column to 'date'
    df.rename(columns={'message_date': 'date'}, inplace=True)

    users = []
    messages = []  # Changed the variable name to avoid confusion with the loop variable
    for message in df['user_message']:  # Changed to use 'date' column
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # Check if there are user and message parts
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    # Check if the lengths of users and messages lists match the length of the DataFrame
    # print(len(users), len(messages), len(df))

    df['user'] = users
    df['message'] = messages

    # Now try to drop the 'user_message' column
    df.drop(columns=['user_message'], inplace=True)

    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['month_num'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['only_date'] = df['date'].dt.date

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df