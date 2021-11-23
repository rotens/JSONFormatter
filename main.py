from lexer import Lexer, JsonLexingException
from parser_ import Parser, JsonParsingException
from formatter import format_json
import tkinter as tk
import tkinter.scrolledtext as tkscrolled


RED_COLOR = "#FF0000"
GREEN_COLOR = "#00FF00"


class GraphicInterface(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.lexer = Lexer()
        self.parser = Parser()
        self.tokens = []
        self.master = master
        self.pack()
        
        # Labels
        self.lb_input_json = tk.Label(self, text="Input JSON")
        self.lb_input_json.grid(row=0, column=0)

        self.lb_output_json = tk.Label(self, text="Formatted JSON")
        self.lb_output_json.grid(row=0, column=1)

        # Input text
        self.input_text_frame = tk.Frame(self, borderwidth=1, relief="sunken")
        self.input_text = tk.Text(
            self.input_text_frame, width=60, height=45, wrap="none", borderwidth=0)
        textVsb = tk.Scrollbar(
            self.input_text_frame, orient="vertical", command=self.input_text.yview)
        textHsb = tk.Scrollbar(
            self.input_text_frame, orient="horizontal", command=self.input_text.xview)
        self.input_text.configure(
            yscrollcommand=textVsb.set, xscrollcommand=textHsb.set)

        self.input_text.grid(row=0, column=0, sticky="nsew")
        textVsb.grid(row=0, column=1, sticky="ns")
        textHsb.grid(row=1, column=0, sticky="ew")

        self.input_text_frame.grid_rowconfigure(0, weight=1)
        self.input_text_frame.grid_columnconfigure(0, weight=1)

        self.input_text_frame.grid(row=1, column=0)

        # Output text
        self.output_text_frame = tk.Frame(self, borderwidth=1, relief="sunken")
        self.output_text = tk.Text(
            self.output_text_frame, width=60, height=45, wrap="none", borderwidth=0,
            state="disabled")
        textVsb = tk.Scrollbar(
            self.output_text_frame, orient="vertical", command=self.output_text.yview)
        textHsb = tk.Scrollbar(
            self.output_text_frame, orient="horizontal", command=self.output_text.xview)
        self.output_text.configure(
            yscrollcommand=textVsb.set, xscrollcommand=textHsb.set)

        self.output_text.grid(row=0, column=0, sticky="nsew")
        textVsb.grid(row=0, column=1, sticky="ns")
        textHsb.grid(row=1, column=0, sticky="ew")

        self.output_text_frame.grid_rowconfigure(0, weight=1)
        self.output_text_frame.grid_columnconfigure(0, weight=1)

        self.output_text_frame.grid(row=1, column=1)

        self.lb_message = tk.Label(self, text="")
        self.lb_message.grid(row=2, column=0, columnspan=2, sticky=tk.W+tk.E)

        # Left side buttons
        self.buttons_frame = tk.Frame(self, pady=5)
        self.buttons_frame.grid(row=3, column=0)
        self.btn_validate = tk.Button(self.buttons_frame, text="Validate", comman=self.validate)
        self.btn_format = tk.Button(self.buttons_frame, text="Format", command=self.format)
        self.btn_validate.grid(row=0, column=0)
        self.btn_format.grid(row=0, column=1)

        # Right side button
        self.btn_copy = tk.Button(self, text="Copy text", command=self.copy_text)
        self.btn_copy.grid(row=3, column=1)

    def validate(self): 
        input_text = self.input_text.get("1.0", "end-1c")
        if not input_text:
            return False

        try:
            self.tokens = self.lexer.lex(input_text)
            print(input_text)
            print(self.tokens)
        except JsonLexingException as e:
            self.lb_message["text"] = str(e)
            self.lb_message["fg"] = RED_COLOR
            return False

        try:
            self.parser.parse(self.tokens, is_root=True)
        except JsonParsingException as e:
            self.lb_message["text"] = str(e)
            self.lb_message["fg"] = RED_COLOR
            return False

        self.lb_message["text"] = "Valid"
        self.lb_message["fg"] = GREEN_COLOR
        return True

    def format(self):
        self.output_text["state"] = "normal"
        self.output_text.delete("1.0", tk.END)

        if not self.validate():
            return  

        formatted_json = format_json(self.tokens)
        self.output_text.insert(tk.INSERT, formatted_json)
        self.output_text["state"] = "disabled"

    def copy_text(self):
        self.master.clipboard_clear()
        output_text = self.output_text.get("1.0", "end-1c")
        self.master.clipboard_append(output_text)



def main():
    root = tk.Tk()
    root.title("JSON Formatter")
    root.resizable(False, False)
    GraphicInterface(root).mainloop()


if __name__ == "__main__":
    main()