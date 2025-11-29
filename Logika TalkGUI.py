from customtkinter import *
import socket 
import threading
from    PIL import Image
SERVER_NAME ='localhost'
PORT = 8080

class ChatClient(CTk):
    def __init__(self):
        super().__init__()
        self.nicKname = 'Unknown'
        self.title('LOGIKA TALK')
        self.geometry('500x500')
        img  = CTkImage(light_image=Image.open("D:\\логика\\istockphoto-1970631602-612x612.jpg"))
        self.sock = None
        self.running = None
        self.recv_thread = None
        self.nicKnameframe = CTkFrame(self)
        self.nicKnameframe.pack(pady=50)
        #self.image=CTkLabel(self.nicKname,text="", image=img)
        self.nicKname_lb = CTkLabel(
            self.nicKnameframe,text = "Введіть нік нейм",
            text_color='green',
            fg_color="grey",
            bg_color="black"
        )
        self.nicKname_lb.pack(pady=10,padx=10)
        self.nicKname_entry =CTkEntry(
            self.nicKnameframe,width=100,height=50,placeholder_text="Ведіть нік тут"
        )
        self.nicKname_entry.pack(pady=10, padx=10)
        #self.image.pack()
        self.chat_frame = CTkFrame(self,width=500, height=500)
        self.chat_box = CTkTextbox(self.chat_frame,width=450,height=300,state = 'disabled')
        self.chat_box.place(y=20,x=20)
        self.chat_entry = CTkEntry(
            self.chat_frame,
            width=350,
            height=40,
            placeholder_text="Введіть повідомлення",
            border_color="white",
        )
        self.chat_box.configure(text_color="purple")
        self.chat_entry.place(x=20,y=330)
        self.connect_btn =CTkButton(self.nicKnameframe,text ="Увійти у чат", width=140, height=50, command = self.start_chat
        )
        self.connect_btn.pack(pady=10,padx=10)
        self.chat_frame.pack_forget()
        
        self.send_btn = CTkButton(
            self.chat_frame,
            text="Відправити",
            width=120,
            height=50,
            command=self.sent_message,
        )
        self.send_btn.place(x=350,y=330)
        
    def start_chat(self):
        self.nicKname = self.nicKname_entry.get().strip()
        self.nicKname = self.nicKname if self.nicKname else 'Unknown'
        self.nicKnameframe.pack_forget()
        self.chat_frame.place(x=0,y=0)
        self.append_local("[SYSTEM] Спроба підключення")
        threading. Thread(target=self.connect_to_server).start()
    def connect_to_server(self):
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((SERVER_NAME,PORT))
            self.client=client
            self.running = True
            self.append_local(f"[SYSTEM] Підключення до {SERVER_NAME}:{PORT}")
            text = f"{self.nicKname}@{self.nicKname} приєднатися до чату\n"
            self.client.send(text.encode())
            self.recv_thread=threading.Thread(target=self.recv_loop)
            self.recv_thread.   start()
        except Exception as a:
            self.append_local(f"[SYSTEM] [EROR] {a}")
    def append_local(self,text):
        self.chat_box.configure(state='normal')
        self.chat_box.insert(END,self.nicKname+" : "+text+"\n")
        self.chat_box.see(END)
        self.chat_box.configure(state='disabled')
    def sent_message(self):
        text = self.chat_entry.get().strip()
        if not text:
            return
        #self.append_local(text)
        self.client.send((text+"\n").encode())
    
        self.chat_entry.delete(0,END)
    def recv_loop(self):
        buffer=''
        try:
            while self.running:
                text=self.client.recv(4100).decode()
                if not text:
                    break
                buffer+=text
                while "\n" in buffer:
                    line,buffer = buffer.split("\n",1)
                    self.handle_line(line.strip())
        except Exception as e:
            self.append_local(f"[SYSTEM] [ERROR] {e}")
        finally:
            try:
               self.client.close()
            except:
               pass
            self.append_local(f"[SYSTEM] Відєднано від серверу")
    def handle_line(self,line):
        if not line:
            return
        parts = line.splint("@",2)
        if len(parts)>=3 and parts[0] =="TEXT":
            a=parts[1]
            msg=parts[2]
            self.after(0,self.append_local(f'{a}: {msg}'))
        else:
            self.after(0,self.append_local(f'{line}'))
    
window = ChatClient()

window.mainloop()
