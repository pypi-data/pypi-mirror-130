## Import
```import MsTeamsConnector```

## Authorize
`SCOPE` param is optional and set to `.default` as default
```
credentials = {
    'CLIENT_ID': '{client_id}',
    'AUTHORITY': 'https://login.microsoftonline.com/{authority}',
    'USERNAME': '{user}',
    'PASSWORD': '{pass}',
    'SCOPE': [{scope_1}, {scope_2}]
}   
msc = MsTeamsConnector(credentials)  
```

## Send message
Init Message
```
msc.create_message(team_id = team_id, channel_id = channel_id)  
```

Add title
```
msc.add_title('Test Graph API message')  
```

Add HTML text
```
msc.add_text('Test msg using Graph API')
```

Add text with mention
```
msc.add_text('Test msg using Graph API. Mention <at>{User Name}</at>')
```

Set importance level
Can be only `high` or `normal`
```
msc.set_importance('high')
```

Set message to reply
```
msc.set_reply_message(message_id)
```

Send message
```
msc.send_message()
```
