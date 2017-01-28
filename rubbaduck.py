import tkinter
import threading
import time
import random


def setup():
    root = tkinter.Tk()
    root.title("Rubbaduck Instant Messenger")
    root.geometry('640x480')
    canvas = tkinter.Canvas(root, bg='white')
    frame_left = tkinter.Frame(canvas, bg='white')
    frame_right = tkinter.Frame(root, padx=5)
    frame_bottom = tkinter.Frame(canvas)

    vertscroll = tkinter.Scrollbar(canvas, orient='vertical', command=canvas.yview)
    canvas.configure(yscrollcommand=vertscroll.set)

    default_message = tkinter.Label(frame_left, text="Duck: Hi, please explain your problem to me!", bg='#EFEFEF',
                                    fg='black', justify=tkinter.LEFT, anchor=tkinter.W, padx=10, pady=5)

    input_box = tkinter.Text(frame_bottom, bg='white', fg='black', height=3, width=20)
    send_button = tkinter.Button(frame_bottom, text="Send Message", bg='grey', pady=18)
    typing_display = tkinter.Label(frame_bottom)

    user_profile_pic = tkinter.PhotoImage(file="default.png")
    duck_profile_pic = tkinter.PhotoImage(file="duck.png")

    user_profile_pic_box = tkinter.Label(frame_right, image=user_profile_pic, bg='white', relief=tkinter.RIDGE)
    user_profile_pic_box.image = user_profile_pic
    duck_profile_pic_box = tkinter.Label(frame_right, image=duck_profile_pic, bg='white', relief=tkinter.RIDGE)
    duck_profile_pic_box.image = duck_profile_pic

    def duck_reply(message):
        nonlocal frame_left
        nonlocal typing_display

        if message.lower().startswith(('hi ', 'hello ', 'hey ', 'howdy '))\
            or message.lower() in ['hi', 'hello', 'hey', 'howdy']:
            response_choice = 'Hello. What are you working on right now?'
        elif message.endswith('?'):
            response_choice = 'Sorry, I cannot answer questions. I am only here to listen.'
        else:
            responses = ['I see.', 'Interesting.', 'Okay.', 'Uh huh.', 'Right.', 'Ah.']
            response_choice = random.choice(responses)

        typing_display.configure(text='Duck is typing...')

        sleep_time = random.randint(5, 10) / 10.0
        time.sleep(sleep_time)

        duck_message = tkinter.Label(frame_left, fg='black', bg='#EFEFEF', justify=tkinter.LEFT, anchor=tkinter.W,
                                     padx=10, text='Duck: ' + response_choice, pady=5)
        duck_message.pack(fill=tkinter.X)

        typing_display.configure(text='')

    def send_message(event=None):
        nonlocal input_box
        nonlocal frame_left
        nonlocal default_message
        nonlocal typing_display

        message = input_box.get(1.0, tkinter.END).strip()
        if message:
            message_text = '  Me: ' + message
            message_log = default_message.cget('text')

            max_length = 65

            if len(message_text) > max_length:
                message_text_pieces = [message_text[i:i+max_length] for i in range(0, len(message_text), max_length)]
                for i in range(1, len(message_text_pieces)):
                    message_text_pieces[i] = '          ' + message_text_pieces[i]

                message_text = '\n'.join(message_text_pieces)

            new_message = tkinter.Label(frame_left, fg='black', bg='white', justify=tkinter.LEFT, anchor=tkinter.W,
                                        padx=10, pady=5)
            new_message.configure(text=message_text)
            new_message.pack(fill=tkinter.X)

            input_box.delete(1.0, tkinter.END)

            if not typing_display.cget('text'):
                replying_thread = threading.Thread(target=duck_reply, args=(message,))
                replying_thread.start()
                replying_thread = threading.Thread(target=duck_reply, args=(message,))

    def onFrameConfigure(canvas):
        canvas.configure(scrollregion=canvas.bbox("all"))

    def chat_width(event, canvas_frame):
        canvas_width = event.width
        canvas.itemconfig(canvas_frame, width = canvas_width)

    def mouse_scroll(event, canvas):
        if event.delta:
            canvas.yview_scroll(-1*(event.delta/120), 'units')
        else:
            if event.num == 5:
                move = 1
            else:
                move = -1

            canvas.yview_scroll(move, 'units')

    send_button.configure(command=send_message)

    root.bind('<Return>', send_message)
    root.bind('<Configure>', lambda event, canvas=canvas: onFrameConfigure(canvas))
    root.bind_all('<MouseWheel>', lambda event, canvas=canvas: mouse_scroll(event, canvas))
    root.bind_all('<Button-4>', lambda event, canvas=canvas: mouse_scroll(event, canvas))
    root.bind_all('<Button-5>', lambda event, canvas=canvas: mouse_scroll(event, canvas))

    canvas.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=1)
    canvas_frame = canvas.create_window((4, 4), window=frame_left, anchor="nw")
    vertscroll.pack(side=tkinter.RIGHT, fill=tkinter.Y)
    canvas.bind('<Configure>', lambda event, canvas_frame=canvas_frame: chat_width(event, canvas_frame))

    typing_display.pack(side=tkinter.BOTTOM)
    default_message.pack(side=tkinter.TOP, fill=tkinter.X)

    frame_right.pack(side=tkinter.LEFT, fill=tkinter.Y)
    user_profile_pic_box.pack(side=tkinter.BOTTOM)
    duck_profile_pic_box.pack(side=tkinter.TOP)

    frame_bottom.pack(side=tkinter.BOTTOM, fill=tkinter.X)
    input_box.pack(side=tkinter.LEFT, fill=tkinter.X, expand=1, pady=5)
    send_button.pack(side=tkinter.RIGHT, pady=5)

    return root


if __name__ == '__main__':
    root = setup()
    root.mainloop()