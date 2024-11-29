#Password validator
#--Rules
# length 8 or more
# Can't contain any personla info
# Must be alphanumeric(Uppera case, Number and a symbol)


import re
def is_strong_password(password, username, firstname, lastname, email):
    #Checking password length
    if len(password) < 8:
        return False, 'Password must be at least 8 characters long.'
    else:
        personal_info= [username, firstname, lastname, email]
        for info in personal_info:
            if info and info.lower() in password.lower():
                return False, 'Password must not contain personal information.'
        #Checking for personal info
        if re.search(f'(?=.*{username})(?=.*{firstname})(?=.*{lastname})(?=.*{email})', password):
            return False, 'Password must not contain personal information.'
        else:
            #Checking for alphanumeric and symbol
            if re.search('^(?=.*[a-zA-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', password):
                return True, 'Strong password.'
            else:
                return False, 'Password must contain at least one uppercase letter, one number, and one of these special characters. @$!%*?&'