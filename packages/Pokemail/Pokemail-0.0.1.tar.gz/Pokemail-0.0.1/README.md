# Pokemail API

### Example Usage:
    import pokemail


    expected_sender = 'nubonix@example.com'
    poke = Pokemail(username='nubonix')

    # .check_email will return a json response, and within the response,
    #    the key `list` will return a list of emails with their mail_id
    # Call this until you recieve an email from the sender you are expecting an email from
    # `mail_from` is the keyword to use to find the sender from the response
    response_data = poke.check_email()
    
    # If an email has been recieved
    if response_data['list']:
        for mail in response_data['list']:
            if mail['mail_from'] == expected_sender:
                mail_id = mail['mail_id']
                break

    # .fetch_email will get emails from the email box
    # Do as you wish with the email response
    email_response_data = poke.fetch_email(mail_id=mail_id)
