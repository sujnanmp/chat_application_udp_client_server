import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, Entry, Button

class ChatClientGUI:
    def __init__(self, root, client_socket):
        self.root = root
        self.client_socket = client_socket

        self.root.title("Chat App")
        self.chat_area = scrolledtext.ScrolledText(root, state="disabled")
        self.chat_area.pack(padx=10, pady=10)
        
        self.message_entry = Entry(root)
        self.message_entry.pack(padx=10, pady=5, fill=tk.X)
        
        self.send_button = Button(root, text="Send", command=self.send_message)
        self.send_button.pack(padx=10, pady=5)

        self.receive_thread = threading.Thread(target=self.receive_messages)
        self.receive_thread.start()

    def send_message(self):
        message = self.message_entry.get()
        if message:
            self.client_socket.send(message.encode())
            self.message_entry.delete(0, tk.END)

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode()
                self.chat_area.config(state="normal")
                self.chat_area.insert(tk.END, message + "\n")
                self.chat_area.config(state="disabled")
            except:
                break

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define server address and port
server_address = ('127.0.0.1', 12345)

# Connect to the server
client_socket.connect(server_address)

# Create the GUI
root = tk.Tk()
app = ChatClientGUI(root, client_socket)
root.mainloop()
