from lexer import Lexer, JsonLexingException
from parser_ import Parser, JsonParsingException
from formatter import formatter
import tkinter as tk
import tkinter.scrolledtext as tkscrolled


class GraphicInterface(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.pack()
        
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

        self.input_text_frame.grid(row=0, column=0)

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

        self.output_text_frame.grid(row=0, column=1)



def validate(tokens) -> bool:
    parser = Parser()
    try:
        parser.parse(tokens)
    except JsonParsingException:
        return False
    return True


def main():
    lexer = Lexer()
    # tokens = lexer.lex('1')
    tokens = lexer.lex('{"foo": [1, 2, {"bar": 2}, null], "bar": null}')
    # print(tokens)
    # parser = Parser()
    # print(parser.parse(tokens))
    print(tokens)
    print(formatter(tokens))

    root = tk.Tk()
    root.title("JSON Formatter")
    root.resizable(False, False)
    GraphicInterface(root).mainloop()


if __name__ == "__main__":
    main()