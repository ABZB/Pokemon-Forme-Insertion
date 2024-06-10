from tkinter import *

from forme_importation_actual import *
from utilities import *


def pre_check(poke_edit_data):
    
    base_form_index = int(poke_edit_data.base_species_list.index(base_species_entry.get()))
    new_forme_count = int(number_formes_entry.get())
    #print(base_form_index, new_forme_count)print(model_source_index)

    if(model_bool.get() or model_entry.get() == ''):
        #this is not the correct index in the Model file structure, that will be computed later
        model_source_index = base_form_index
    else:
        model_source_index = poke_edit_data.model_source_list.index(model_entry.get())
    
    if(personal_bool.get() or personal_entry.get() == ''):
        personal_source_index = base_form_index
    else:
        personal_source_index = poke_edit_data.master_formes_list.index(personal_entry.get())
    
    if(levelup_bool.get() or levelup_entry.get() == ''):
        levelup_source_index = base_form_index
    else:
        levelup_source_index = poke_edit_data.master_formes_list.index(levelup_entry.get())
    
    if(evolution_bool.get() or evolution_entry.get() == ''):
        evolution_source_index = base_form_index
    else:
        evolution_source_index = poke_edit_data.master_formes_list.index(evolution_entry.get())
    
    if(not(isinstance(base_form_index, int))):
        print("Species is not an integer!")
        return
    elif(not(isinstance(new_forme_count, int))):
        print("Formes to add is not an integer!")
        return
    elif(not(isinstance(model_source_index, int))):
        print("Model source is not an integer!")
        return
    elif(not(isinstance(personal_source_index, int))):
        print("Personal source is not an integer!")
        return
    elif(not(isinstance(levelup_source_index, int))):
        print("Levelup source is not an integer!")
        return
    elif(not(isinstance(evolution_source_index, int))):
        print("Evolution source is not an integer!")
        return

    #print(model_source_index)
    poke_edit_data = add_new_forme_execute(poke_edit_data, base_form_index, new_forme_count, model_source_index, personal_source_index, levelup_source_index , evolution_source_index, model_bool.get())
    
    return(poke_edit_data)

root = Tk()
root.title('Pokemon Forme Insertion V.2.0')
root.geometry('950x300')

#root.iconbitmap(BitmapImage(title_icon_data))

poke_edit_data = Pokedata()

model_bool = BooleanVar()
personal_bool = BooleanVar()
levelup_bool = BooleanVar()
evolution_bool = BooleanVar()

def update_stam(poke_edit_data, input_list, current_list, input_listbox, input_entry):
    
    
    typed = model_entry.get()
    if typed == '':
        #reset everything
        data = poke_edit_data.model_source_list.copy()
    else:
        data = []
        for item in poke_edit_data.current_model_source_list:
            if typed.lower() in item.lower():
                data.append(item)
    poke_edit_data.current_model_source_list = data
    update(data, model_listbox)
    

    #get what was tuped
    typed = input_entry.get()

    if typed == '':
        #full list
        data = input_list.copy()
        #print('nothin, ', data)
    else:
        data = []
        for item in input_list:
            if typed.lower() in item.lower():
                data.append(item)
        data = input_list.copy()
        #print('something, ', data)
        
    current_list = data
    
    
    update(data, input_listbox)
    return(poke_edit_data)

def update(data, input_listbox):
    
    
    #clear list
    input_listbox.delete(0, END)
    for item in data:
        input_listbox.insert(END, item)


#update "Select Species" based on double-clicking in list
def fillout_base_species(e):
    try:
        selection = poke_edit_data.current_base_species_list[base_species_listbox.curselection()[0]]
        base_species_entry.delete(0, END)
        base_species_entry.insert(END, selection)
        check_base_species(e)
    except Exception as error:
        print('You might have double-clicked on an empty row after the last valid selection (tkinter does this sometimes, working on a solution.)', error)

#update search list for base species
def check_base_species(e):
    typed = base_species_entry.get()
    if typed == '':
        #reset everything
        data = poke_edit_data.base_species_list.copy()
    else:
        data = []
        for item in poke_edit_data.current_base_species_list:
            if typed.lower() in item.lower():
                data.append(item)
    poke_edit_data.current_base_species_list = data
    update(data, base_species_listbox)


#update "Custom Personal" based on double-clicking in list
def fillout_personal(e):
    try:
        selection = poke_edit_data.current_personal_list[personal_listbox.curselection()[0]]
        personal_entry.delete(0, END)
        personal_entry.insert(END, selection)
        check_personal(e)
    except Exception as error:
        print('You might have double-clicked on an empty row after the last valid selection (tkinter does this sometimes, working on a solution.)', error)
    
#update listbox for personal source
def check_personal(e):
    typed = personal_entry.get()
    if typed == '':
        #reset everything
        data = poke_edit_data.master_formes_list.copy()
    else:
        data = []
        for item in poke_edit_data.current_personal_list:
            if typed.lower() in item.lower():
                data.append(item)
    poke_edit_data.current_personal_list = data
    update(data, personal_listbox)

#update "Custom Levelup" based on double-clicking in list
def fillout_levelup(e):
    try:    
        selection = poke_edit_data.current_levelup_list[levelup_listbox.curselection()[0]]
        levelup_entry.delete(0, END)
        levelup_entry.insert(END, selection)
        check_levelup(e)
    except Exception as error:
        print('You might have double-clicked on an empty row after the last valid selection (tkinter does this sometimes, working on a solution.)', error)
    
#update listbox for levelup source
def check_levelup(e):
    typed = levelup_entry.get()
    if typed == '':
        #reset everything
        data = poke_edit_data.master_formes_list.copy()
    else:
        data = []
        for item in poke_edit_data.current_levelup_list:
            if typed.lower() in item.lower():
                data.append(item)
    poke_edit_data.current_levelup_list = data
    update(data, levelup_listbox)

#update "Custom Evolution" based on double-clicking in list
def fillout_evolution(e):
    try:
        selection = poke_edit_data.current_evolution_list[evolution_listbox.curselection()[0]]
        evolution_entry.delete(0, END)
        evolution_entry.insert(END, selection)
        check_evolution(e)
    except Exception as error:
        print('You might have double-clicked on an empty row after the last valid selection (tkinter does this sometimes, working on a solution.)', error)

#update listbox for evolution source
def check_evolution(e):
    typed = evolution_entry.get()
    if typed == '':
        #reset everything
        data = poke_edit_data.master_formes_list.copy()
    else:
        data = []
        for item in poke_edit_data.current_evolution_list:
            if typed.lower() in item.lower():
                data.append(item)
    poke_edit_data.current_evolution_list = data
    update(data, evolution_listbox)

#update "Custom Model" based on double-clicking in list
def fillout_model(e):
    try:
        selection = poke_edit_data.current_model_source_list[model_listbox.curselection()[0]]
        model_entry.delete(0, END)
        model_entry.insert(END, selection)
        check_model
    except Exception as error:
        print('You might have double-clicked on an empty row after the last valid selection (tkinter does this sometimes, working on a solution.)', error)
 

#update listbox for model source
def check_model(e):
    typed = model_entry.get()
    if typed == '':
        #reset everything
        data = poke_edit_data.model_source_list.copy()
    else:
        data = []
        for item in poke_edit_data.current_model_source_list:
            if typed.lower() in item.lower():
                data.append(item)
    poke_edit_data.current_model_source_list = data
    update(data, model_listbox)

def set_games_checklist(gameinput):
    games_temp.set(gameinput)

#update all listboxes
def update_all_listboxes(poke_edit_data):
    update_stam(poke_edit_data, poke_edit_data.model_source_list, poke_edit_data.current_model_source_list, model_listbox, model_entry)
    update_stam(poke_edit_data, poke_edit_data.master_formes_list, poke_edit_data.current_evolution_list, evolution_listbox, evolution_entry)
    update_stam(poke_edit_data, poke_edit_data.master_formes_list, poke_edit_data.current_levelup_list, levelup_listbox, levelup_entry)
    update_stam(poke_edit_data, poke_edit_data.master_formes_list, poke_edit_data.current_personal_list, personal_listbox, personal_entry)
    update_stam(poke_edit_data, poke_edit_data.base_species_list, poke_edit_data.current_base_species_list, base_species_listbox, base_species_entry)
    return(poke_edit_data)

for x in range(5):
    Grid.rowconfigure(root, x, weight = 1)

for y in range(7):
    Grid.columnconfigure(root, y, weight = 1)


#load/save config
cfg_load = Button(root, text = 'Load CFG', command = lambda: [load_game_cfg(poke_edit_data), set_games_checklist(poke_edit_data.game), update_all_listboxes(poke_edit_data)], height = 2, width = 18, pady = 5, padx = 7)
cfg_load.grid(row = 0, column = 0, sticky="ew")


cfg_save = Button(root, text = 'Save CFG & CSV', command = lambda: save_game_cfg(poke_edit_data, games_temp.get()), height = 2, width = 18, pady = 5, padx = 7)
cfg_save.grid(row = 1, column = 0, sticky="ew")


#select game
games = ["XY", "ORAS", "SM", "USUM"]

games_temp = StringVar(root)
games_temp.set("Select Game")
game_select = OptionMenu(root, games_temp, *games)
game_select.grid(row = 0, column = 1, sticky="ew")


#load Model
model_load = Button(root, text = 'Select Model Path', command = lambda: [choose_GARC(poke_edit_data, "Model", games_temp.get()), update(poke_edit_data.model_source_list, model_listbox)], height = 2, width = 18, pady = 5, padx = 7)
model_load.grid(row = 0, column = 2, sticky="ew")

#load Personal
personal_load = Button(root, text = 'Select Personal Path', command = lambda: [choose_GARC(poke_edit_data, "Personal", games_temp.get()), update(poke_edit_data.base_species_list, base_species_listbox), update(poke_edit_data.master_formes_list, personal_listbox), update(poke_edit_data.master_formes_list, levelup_listbox), update(poke_edit_data.master_formes_list, evolution_listbox), update(poke_edit_data.model_source_list, model_listbox)], height = 2, width = 18, pady = 5, padx = 7)
personal_load.grid(row = 0, column = 3, sticky="ew")

#load Levelup
levelup_load = Button(root, text = 'Select Levelup Path', command = lambda: choose_GARC(poke_edit_data, "Levelup", games_temp.get()), height = 2, width = 18, pady = 5, padx = 7)
levelup_load.grid(row = 0, column = 4, sticky="ew")

#load Evolution
evolution_load = Button(root, text = 'Select Evolution Path', command = lambda: choose_GARC(poke_edit_data, "Evolution", games_temp.get()), height = 2, width = 18, pady = 5, padx = 7)
evolution_load.grid(row = 0, column = 5, sticky="ew")



#Base Species Selection
base_species_label = Label(root, text = "Select Species", width = 12, padx = 7)
base_species_label.grid(row = 2, column = 0, sticky="nsew")

base_species_entry = Entry(root, width = 18)
base_species_entry.grid(row = 3, column = 0, sticky="nsew")

base_species_listbox = Listbox(root, width = 18)
base_species_listbox.grid(row = 4, column = 0, sticky="nsew")

update(poke_edit_data.base_species_list, base_species_listbox)

base_species_listbox.bind("<Double-1>", fillout_base_species)
base_species_entry.bind("<KeyRelease>", check_base_species)


#Model Selection

model_checkbutton = Checkbutton(root, text = 'Same as Species', variable = model_bool, onvalue = True, offvalue = False)
model_checkbutton.grid(row = 1, column = 2, sticky="nsew")
model_checkbutton.select()

model_label = Label(root, text = "Custom Model", width = 12, padx = 3)
model_label.grid(row = 2, column = 2, sticky="nsew")

model_entry = Entry(root, width = 18)
model_entry.grid(row = 3, column = 2, sticky="nsew")

model_listbox = Listbox(root, width = 18)
model_listbox.grid(row = 4, column = 2, sticky="nsew")

update(poke_edit_data.model_source_list, model_listbox)

model_listbox.bind("<Double-1>", fillout_model)
model_entry.bind("<KeyRelease>", check_model)


#Personal Selection

personal_checkbutton = Checkbutton(root, text = 'Same as Species', variable = personal_bool, onvalue = True, offvalue = False)
personal_checkbutton.grid(row = 1, column = 3, sticky="nsew")
personal_checkbutton.select()

personal_label = Label(root, text = "Custom Personal", width = 12, padx = 3)
personal_label.grid(row = 2, column = 3, sticky="nsew")

personal_entry = Entry(root, width = 18)
personal_entry.grid(row = 3, column = 3, sticky="nsew")

personal_listbox = Listbox(root, width = 18)
personal_listbox.grid(row = 4, column = 3, sticky="nsew")

update(poke_edit_data.master_formes_list, personal_listbox)

personal_listbox.bind("<Double-1>", fillout_personal)
personal_entry.bind("<KeyRelease>", check_personal)


#Levelup Selection

levelup_checkbutton = Checkbutton(root, text = 'Same as Species', variable = levelup_bool, onvalue = True, offvalue = False)
levelup_checkbutton.grid(row = 1, column = 4, sticky="nsew")
levelup_checkbutton.select()

levelup_label = Label(root, text = "Custom Levelup", width = 12, padx = 3)
levelup_label.grid(row = 2, column = 4, sticky="nsew")

levelup_entry = Entry(root, width = 18)
levelup_entry.grid(row = 3, column = 4, sticky="nsew")

levelup_listbox = Listbox(root, width = 18)
levelup_listbox.grid(row = 4, column = 4, sticky="nsew")

update(poke_edit_data.master_formes_list, levelup_listbox)

levelup_listbox.bind("<Double-1>", fillout_levelup)
levelup_entry.bind("<KeyRelease>", check_levelup)

#Evolution Selection

evolution_checkbutton = Checkbutton(root, text = 'Same as Species', variable = evolution_bool, onvalue = True, offvalue = False)
evolution_checkbutton.grid(row = 1, column = 5, sticky="nsew")
evolution_checkbutton.select()

evolution_label = Label(root, text = "Custom Evolution", width = 12, padx = 4)
evolution_label.grid(row = 2, column = 5, sticky="nsew")

evolution_entry = Entry(root, width = 18)
evolution_entry.grid(row = 3, column = 5, sticky="nsew")

evolution_listbox = Listbox(root, width = 18)
evolution_listbox.grid(row = 4, column = 5, sticky="nsew")

update(poke_edit_data.master_formes_list, evolution_listbox)

evolution_listbox.bind("<Double-1>", fillout_evolution)
evolution_entry.bind("<KeyRelease>", check_evolution)

#CSV file path Selection

load_pokelist_csv_button = Button(root, text = 'Load CSV', command = lambda: [user_prompt_load_CSV(poke_edit_data, 'Pokemon Names and Files'), update_all_listboxes(poke_edit_data)], height = 2, width = 18, pady = 5, padx = 7)
load_pokelist_csv_button.grid(row = 0, column = 6, sticky="ew")

save_pokelist_csv_button = Button(root, text = 'Save CSV', command = lambda: [user_prompt_write_CSV(poke_edit_data, 'Pokemon Names and Files'), update_all_listboxes(poke_edit_data)], height = 2, width = 18, pady = 5, padx = 7)
save_pokelist_csv_button.grid(row = 1, column = 6, sticky="ew")

create_pokelist_csv_button = Button(root, text = 'Create/Reset CSV', command = lambda: [create_refresh_CSV(poke_edit_data, 'Pokemon Names and Files', games_temp.get()), update_all_listboxes(poke_edit_data)], height = 2, width = 18, pady = 5, padx = 7)
create_pokelist_csv_button.grid(row = 4, column = 6, sticky="ew")


#Number of New Formes
number_formes_label = Label(root, text = "# Formes To Add", width = 12, padx = 4)
number_formes_label.grid(row = 2, column = 1, sticky="nsew")

number_formes_entry = Entry(root, width = 12)
number_formes_entry.grid(row = 3, column = 1)

#Run Insertion
execute_button = Button(root, text = 'Insert Forme(s)', command = lambda: [pre_check(poke_edit_data), update_all_listboxes(poke_edit_data)], height = 2, width = 12, pady = 5, padx = 7)
execute_button.grid(row = 4, column = 1, sticky="ew")



#print("help")
root.mainloop()