def make_thread_message_into_thread(thread_messages):
    all_thread = []
    sub_thread = []
    previous_thread_id = None
    for thread_message in thread_messages:
        thread_id = thread_message[0]
        if thread_id != previous_thread_id:
            sub_thread.append(thread_message)
        else:
            all_thread.append(sub_thread)
            sub_thread = []
            sub_thread.append(thread_message)
    return all_thread