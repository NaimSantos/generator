import tkinter as tk
from tkinter import ttk, messagebox
from common import *
from card_manager import *
from sqlite_manager import *
#from time import strftime



# To clear placeholder text on click
def clear_placeholder(event, widget, default_text):
    current_text = widget.get("1.0", "end-1c")
    if current_text == default_text:
        widget.delete("1.0", "end")
        widget.config(fg="black")  # Change text color to black

# To restore placeholder text if box is empty
def restore_placeholder(event, widget, default_text):
    current_text = widget.get("1.0", "end-1c").strip()
    if current_text == "":
        widget.insert("1.0", default_text)
        widget.config(fg="gray")  # Change text color to gray

def CreateMainScreen(window):
    frame = ttk.Frame(window)
    frame.grid(sticky="nsew")
    # attempt to make the window expand properly:
    for i in range(7):
        frame.grid_rowconfigure(i, weight=1)
    for j in range(4):
        frame.grid_columnconfigure(j, weight=1)

    SelectedOT = tk.StringVar()

    # Placeholder text and default color
    default_outputfile_text = "Enter the name of the output file..."
    default_packcode_text = "Enter set/pack code (for example, ROTA is 101206XXX)"
    default_urls_text = "Enter Yugipedia page(s)..."

    # Output file label and text box with placeholder
    label_outputfile = ttk.Label(frame, text="Output file:", justify="left", width=20)
    label_outputfile.grid(row=0, column=0, pady=5, sticky="w")

    textbox_outputfile = tk.Text(frame, height=1, width=60, bg="white", fg="gray")
    textbox_outputfile.insert("1.0", default_outputfile_text)
    textbox_outputfile.grid(row=0, column=1, columnspan=3, padx=10, sticky="ew")

    textbox_outputfile.bind("<FocusIn>", lambda event: clear_placeholder(event, textbox_outputfile, default_outputfile_text))
    textbox_outputfile.bind("<FocusOut>", lambda event: restore_placeholder(event, textbox_outputfile, default_outputfile_text))

    # Set/pack code label and text box with placeholder
    label_packcode = ttk.Label(frame, text="Code of the set/pack:", justify="left", width=20)
    label_packcode.grid(row=2, column=0, pady=10, sticky="w")

    textbox_packcode = tk.Text(frame, height=1, width=60, bg="white", fg="gray")
    textbox_packcode.insert("1.0", default_packcode_text)
    textbox_packcode.grid(row=2, column=1, columnspan=3, padx=10, sticky="ew")

    textbox_packcode.bind("<FocusIn>", lambda event: clear_placeholder(event, textbox_packcode, default_packcode_text))
    textbox_packcode.bind("<FocusOut>", lambda event: restore_placeholder(event, textbox_packcode, default_packcode_text))

    # Yugipedia pages label and text box with placeholder
    label_urls = ttk.Label(frame, text="Yugipedia pages:", anchor='sw', width=20)
    label_urls.grid(row=3, column=0, sticky="w")

    textbox_urls = tk.Text(frame, height=10, width=60, bg="white", fg="gray")
    textbox_urls.insert("1.0", default_urls_text)
    textbox_urls.grid(row=4, column=1, columnspan=3, padx=10, pady=5, sticky="nsew")

    textbox_urls.bind("<FocusIn>", lambda event: clear_placeholder(event, textbox_urls, default_urls_text))
    textbox_urls.bind("<FocusOut>", lambda event: restore_placeholder(event, textbox_urls, default_urls_text))

    # Radio buttons for the product type (official, not released, rush)
    label_typeofcards = ttk.Label(frame, text="Type of the cards:", justify="left", width=20)
    label_typeofcards.grid(row=1, column=0, pady=5, sticky="w")

    radbutton_official = ttk.Radiobutton(frame, text="Official cards already released", variable=SelectedOT, value=1)
    radbutton_official.grid(row=1, column=1, sticky="w")

    radbutton_unreleased = ttk.Radiobutton(frame, text="Unreleased official cards", variable=SelectedOT, value=2)
    radbutton_unreleased.grid(row=1, column=2, sticky="w")

    radbutton_rush = ttk.Radiobutton(frame, text="Rush cards", variable=SelectedOT, value=3)
    radbutton_rush.grid(row=1, column=3, sticky="w")

    #  CDB generation button
    def enable_generate_button():
        outputfile = GetTextFromWidget(textbox_outputfile).strip()
        packcode = GetTextFromWidget(textbox_packcode).strip()
        urls = GetTextFromWidget(textbox_urls).strip()
        if outputfile and packcode and urls and SelectedOT.get():
            button_generatecdb.config(state="normal")
        else:
            button_generatecdb.config(state="disabled")

    button_generatecdb = ttk.Button(frame, text="Generate cdb", width=20,
                                    command=lambda: GenerateCDB(
                                        GetTextFromWidget(textbox_outputfile),
                                        SelectedOT.get(),
                                        GetTextFromWidget(textbox_packcode),
                                        GetTextFromWidget(textbox_urls)
                                    ))
    button_generatecdb.grid(row=6, column=3, pady=5, sticky="e")
    button_generatecdb.config(state="disabled")  # Initially disable the button

    # Validate fields whenever text is changed
    textbox_outputfile.bind("<KeyRelease>", lambda event: enable_generate_button())
    textbox_packcode.bind("<KeyRelease>", lambda event: enable_generate_button())
    textbox_urls.bind("<KeyRelease>", lambda event: enable_generate_button())
    radbutton_official.bind("<ButtonRelease-1>", lambda event: enable_generate_button())
    radbutton_unreleased.bind("<ButtonRelease-1>", lambda event: enable_generate_button())
    radbutton_rush.bind("<ButtonRelease-1>", lambda event: enable_generate_button())

    # A quit button:
    button_quit = ttk.Button(frame, text="Quit", command=window.destroy)
    button_quit.grid(row=6, column=0, pady=5, padx=5, sticky="w")


def main():
    mainscreen = tk.Tk()
    mainscreen.title("Automatic Database Generator")
    mainscreen.grid_rowconfigure(0, weight=1)
    mainscreen.grid_columnconfigure(0, weight=1)
    
    CreateMainScreen(mainscreen)
    mainscreen.mainloop()

def GenerateCDB(file_name,producttype,baseset,urls):

    baseID=ReturnBaseIDOrNone(baseset)
    file_name=AppendCDBToFileName(file_name)
    DeleteFile(file_name)
    CreateNewDatabase(file_name)

    urls = urls.split('\n')
    for url in urls:
        page,title=GetCardInfoAndPageTitle(url)
        print("title is ", title)
        cardobject=FillCardObjectFromCardInfo(page,title,baseID,producttype)
        InsertIntoDatabase(file_name,cardobject)
    print("Finished!")
    messagebox.showinfo("Success", "CDB generated successfully!")

def GetTextFromWidget(text_widget):
    return text_widget.get("1.0", "end-1c")

if __name__ == "__main__":
    main()
