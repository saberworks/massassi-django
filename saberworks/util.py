def gather_error_messages(form):
    messages = []

    for key, error_list in form.errors.items():
        messages.append("{}: {}".format(key, "\n".join(error_list)))
    
    return messages
