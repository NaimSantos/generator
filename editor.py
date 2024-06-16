from tkinter import *
from tkinter.ttk import *
from common import *
from yugipedia import *
from cdb_construction import *
#from time import strftime

def main():
   StartApplication()

def StartApplication():
    mainscreen = Tk()
    mainscreen.title("Automatic Database Generator")
    CreateMainButtons(mainscreen)
    mainscreen.mainloop()

def get_text_from_widget(text_widget):
    raw_text = text_widget.get("1.0", "end-1c")
    #print("Exibindo o texto recebido:\n\n\n")
    #print(raw_text)
    return raw_text

def GenerateCDB(file_name,producttype,baseset,urls):

    baseID=convert_to_integer_or_return_original(baseset[:6])

    file_name=append_cdb(file_name)
    delete_file(file_name)
    create_new_database(file_name)

    urls = urls.split('\n')
    for url in urls:
        print(url)
        page,title=Get_Data_From_Page(url)
        card_text,card_data=GenerateDataFromCardInfo(page,title,baseID,producttype)
        insert_into_database(file_name,card_text,card_data)

def CreateMainButtons(window):
    frame = Frame(window)
    frame.grid()

    SelectedOT = StringVar() 
    #Exit button

    #Arquivo de saida:
    label_outputfile = Label(
        frame,
        text="Output file:",
        justify="left",
        width=20,
    )
    label_outputfile.grid(row=0, column=0, pady=5)

    textbox_outputfile =Text(
        frame,
        height = 1,
        width = 60,
        bg = "white"
    )
    textbox_outputfile.grid(row=0, column=1, columnspan=3, padx=10)

    #Tipo de carta:
    label_typeofcards=Label(
        frame,
        text="Type of the cards:",
        justify="left",
        width=20,
    )
    label_typeofcards.grid(row=1, column=0, pady=5)

    radbutton_official = Radiobutton (
        frame,
        text="Official cards already released",
        variable=SelectedOT,
        val=1
    )
    radbutton_official.grid(row=1, column=1)

    radbutton_unreleased = Radiobutton (
        frame,
        text="Unreleased official cards",
        variable=SelectedOT,
        val=2
    )
    radbutton_unreleased.grid(row=1, column=2)

    radbutton_rush = Radiobutton (
        frame,
        text="Rush cards",
        variable=SelectedOT,
        val=3
    )
    radbutton_rush.grid(row=1, column=3)
 
    #Informaçao do pack
    label_packcode = Label(
        frame,
        text="Code of the set/pack:",
        justify="left",
        width=20,
    )
    label_packcode.grid(row=2, column=0, pady=10)

    textbox_packcode =Text(
        frame,
        height = 1,
        width = 60,
        bg = "white"
    )
    textbox_packcode.grid(row=2, column=1, columnspan=3, padx=10)

    #Links:
    label_urls=Label(
        frame,
        text="Yugipedia pages: ",
        anchor='sw',
        width=20,
    )
    label_urls.grid(row=3, column=0)

    textbox_urls =Text(
        frame,
        height = 10,
        width = 60,
        bg = "white"
    )
    textbox_urls.grid(row=4, column=1, columnspan=3, padx=10)

    #Geraçao do cdb:
    button_generatecdb=Button(
        frame,
        text="Generate cdb",
        width = 20,
        command=lambda: GenerateCDB(
                    get_text_from_widget(textbox_outputfile),
                    SelectedOT.get(),
                    get_text_from_widget(textbox_packcode),
                    get_text_from_widget(textbox_urls),
                    )
    )
    button_generatecdb.grid(row=6, column=3, rowspan=2, columnspan=2, pady=10)
    #Encerrar:
    quitbutton=Button(
        frame,
        text="Quit",
        command=window.destroy,
        width = 10,
    )
    quitbutton.grid(row=6, column=0, rowspan=2, pady=10)


if __name__ == "__main__":
    main()
