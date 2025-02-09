from tkinter import *
from tkinter import ttk
from forme_importation_actual import *
from utilities import *


def pre_check(poke_edit_data):
    
    #get index of base species
    try:
        base_form_index = int(poke_edit_data.base_species_list.index(base_species_combobox.get().title()))
    except:
        print('Error,',base_species_combobox.get(),'not found.')
        return

    #number of formes to add
    new_forme_count = int(number_formes_entry.get())


    #model
    try:
        if(model_bool.get() or model_combobox.get() == ''):
            #this is not the correct index in the Model file structure, that will be computed later
            model_source_index = base_form_index
        else:
            model_source_index = int(poke_edit_data.base_species_list.index(model_combobox.get().title()))
    except:
        print('Error,',model_combobox.get(),'not found.')
        return

    #personal
    try:
        if(personal_bool.get() or personal_combobox.get() == ''):
            #this is not the correct index in the Model file structure, that will be computed later
            personal_source_index = base_form_index
        else:
            personal_source_index = int(poke_edit_data.base_species_list.index(personal_combobox.get().title()))
    except:
        print('Error,',personal_combobox.get(),'not found.')
        return

    #levelup
    try:
        if(levelup_bool.get() or levelup_combobox.get() == ''):
            #this is not the correct index in the Model file structure, that will be computed later
            levelup_source_index = base_form_index
        else:
            levelup_source_index = int(poke_edit_data.base_species_list.index(levelup_combobox.get().title()))
    except:
        print('Error,',levelup_combobox.get(),'not found.')
        return

    #evolution
    try:
        if(evolution_bool.get() or evolution_combobox.get() == ''):
            #this is not the correct index in the Model file structure, that will be computed later
            evolution_source_index = base_form_index
        else:
            evolution_source_index = int(poke_edit_data.base_species_list.index(evolution_combobox.get().title()))
    except:
        print('Error,',evolution_combobox.get(),'not found.')
        return
    
    #if skip_model_creation_bool is true, checkbox is unclicked, and we want to try skipping model insertion. If it's false (as per default), just set to false, no need for further check
    if(skip_model_creation_bool.get()):
        poke_edit_data, skip_model_insertion, update_forme_count = check_adding_without_models_works(poke_edit_data, base_form_index, new_forme_count)
        #if the above check function returned false, something is not quite right, abort
        if(not(skip_model_insertion)):
            return(poke_edit_data)
    else:
        skip_model_insertion = False
        update_forme_count = 0


    #check the source model for possible issues
    
    #get the model index
    if(model_bool.get()):
        model_source_index_row = find_rows_with_column_matching(poke_edit_data.master_list_csv, 3, personal_source_index)[0]
    else:
        model_source_index_row = find_rows_with_column_matching(poke_edit_data.master_list_csv, 4, model_source_index)[0]

    if(int(poke_edit_data.master_list_csv[model_source_index_row][5]) == 0 and int(poke_edit_data.master_list_csv[model_source_index_row][6]) == 0):
        print('Bitflag check clear\n')
    else:
        print('\nIf bitflags of the selected model are not 0, it is possible that using this source will cause glitches.\nIt is STRONGLY recommended that you confirm you have backups before you proceed.\nBitflag is ', poke_edit_data.master_list_csv[model_source_index_row][5], poke_edit_data.master_list_csv[model_source_index_row][6])
        while True:
            continue_bool = input('\nDo you wish to proceed? Y/N\n')
            if(continue_bool in {'y', 'Y'}):
                break
            elif(continue_bool in {'n', 'N'}):
                return(poke_edit_data)
            print('Invalid entry')



    #print(model_source_index)
    poke_edit_data = add_new_forme_execute(poke_edit_data, base_form_index, new_forme_count, model_source_index, personal_source_index, levelup_source_index , evolution_source_index, model_bool.get(), skip_model_insertion, update_forme_count)
    
    return(poke_edit_data)

root = Tk()
root.title('Pokemon Forme Insertion V.' + version)
root.geometry('1250x200')

poke_edit_data = Pokedata()

model_bool = BooleanVar()
personal_bool = BooleanVar()
levelup_bool = BooleanVar()
evolution_bool = BooleanVar()
skip_model_creation_bool = BooleanVar()

def set_games_checklist(gameinput):
    games_temp.set(gameinput)

def update_non_model_lists(poke_edit_data):

    personal_combobox.config(value = poke_edit_data.master_formes_list)
    evolution_combobox.config(value = poke_edit_data.master_formes_list)
    levelup_combobox.config(value = poke_edit_data.master_formes_list)
    
    base_species_combobox.config(value = poke_edit_data.base_species_list)

def update_model_list_for_box(poke_edit_data):
    model_combobox.config(value = poke_edit_data.model_source_list)



#these are ugly, need to figure out passing event to consolidate
def base_species_combobox_search(event):
    value = event.widget.get()
    if(value == ''):
        base_species_combobox['value'] = poke_edit_data.base_species_list

    else:
        data = []

        for item in poke_edit_data.base_species_list:
            if(value.lower() in item.lower()):
                data.append(item)
            #sets combobox selected value if equal
            if(value.lower() == item.lower()):
                base_species_combobox.set(value.title())
            base_species_combobox['value'] = data

def search_combobox_event(event, value, name):

    if(value == ''):
        name['value'] = poke_edit_data.master_formes_list

    else:
        data = []

        for item in poke_edit_data.master_formes_list:
            if(value.lower() in item.lower()):
                data.append(item)
            #sets combobox selected value if equal
            if(value.lower() == item.lower()):
                name.set(value.title())
            name['value'] = data


def personal_combobox_search(event):
    value = event.widget.get()
    search_combobox_event(event, value, personal_combobox)

def levelup_combobox_search(event):
    value = event.widget.get()
    search_combobox_event(event, value, levelup_combobox)

def evolution_combobox_search(event):
    value = event.widget.get()
    search_combobox_event(event, value, evolution_combobox)

def model_combobox_search(event):
    value = event.widget.get()

    if(value == ''):
        model_combobox['value'] = poke_edit_data.model_source_list

    else:
        data = []

        for item in poke_edit_data.model_source_list:
            if(value.lower() in item.lower()):
                data.append(item)
            #sets combobox selected value if equal
            if(value.lower() == item.lower()):
                model_combobox.set(value.title())
            model_combobox['value'] = data

for x in range(5):
    Grid.rowconfigure(root, x, weight = 1)

for y in range(7):
    Grid.columnconfigure(root, y, weight = 1)


#load/save config
cfg_load = Button(root, text = 'Load CFG & CSV', command = lambda: [load_game_cfg(poke_edit_data), set_games_checklist(poke_edit_data.game), update_non_model_lists(poke_edit_data), update_model_list_for_box(poke_edit_data)], height = 2, width = 18, pady = 5, padx = 7)
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
model_load = Button(root, text = 'Select Model GARC', command = lambda: [choose_GARC(poke_edit_data, "Model", games_temp.get()), update_model_list_for_box(poke_edit_data)], height = 2, width = 18, pady = 5, padx = 7)
model_load.grid(row = 0, column = 2, sticky="ew")

#load Personal
personal_load = Button(root, text = 'Select Personal GARC', command = lambda: [choose_GARC(poke_edit_data, "Personal", games_temp.get()), update_non_model_lists(poke_edit_data), update_model_list_for_box(poke_edit_data)], height = 2, width = 18, pady = 5, padx = 7)
personal_load.grid(row = 0, column = 3, sticky="ew")

#load Levelup
levelup_load = Button(root, text = 'Select Levelup GARC', command = lambda: choose_GARC(poke_edit_data, "Levelup", games_temp.get()), height = 2, width = 18, pady = 5, padx = 7)
levelup_load.grid(row = 0, column = 4, sticky="ew")

#load Evolution
evolution_load = Button(root, text = 'Select Evolution GARC', command = lambda: choose_GARC(poke_edit_data, "Evolution", games_temp.get()), height = 2, width = 18, pady = 5, padx = 7)
evolution_load.grid(row = 0, column = 5, sticky="ew")


#Base Species Selection
base_species_label = Label(root, text = "Select Species", height = 2, width = 12, padx = 4)
base_species_label.grid(row = 2, column = 0, sticky="nsew")


base_species_combobox = ttk.Combobox(root, value = [], width = 18)
base_species_combobox.grid(row = 3, column = 0, sticky="new")

base_species_combobox.bind('<KeyRelease>', base_species_combobox_search)


#Model Selection

model_checkbutton = Checkbutton(root, text = 'Same as Species', variable = model_bool, onvalue = True, offvalue = False)
model_checkbutton.grid(row = 1, column = 2, sticky="nsew")
model_checkbutton.select()

model_label = Label(root, text = "Custom Model", height = 2, width = 12, padx = 4)
model_label.grid(row = 2, column = 2, sticky="nsew")

model_combobox = ttk.Combobox(root, value = [], width = 18)
model_combobox.grid(row = 3, column = 2, sticky="new")

model_combobox.bind('<KeyRelease>', model_combobox_search)

#Personal Selection

personal_checkbutton = Checkbutton(root, text = 'Same as Species', variable = personal_bool, onvalue = True, offvalue = False)
personal_checkbutton.grid(row = 1, column = 3, sticky="nsew")
personal_checkbutton.select()

personal_label = Label(root, text = "Custom Personal", height = 2, width = 12, padx = 4)
personal_label.grid(row = 2, column = 3, sticky="nsew")


personal_combobox = ttk.Combobox(root, value = [], width = 18)
personal_combobox.grid(row = 3, column = 3, sticky="new")

personal_combobox.bind('<KeyRelease>', personal_combobox_search)

#Levelup Selection

levelup_checkbutton = Checkbutton(root, text = 'Same as Species', variable = levelup_bool, onvalue = True, offvalue = False)
levelup_checkbutton.grid(row = 1, column = 4, sticky="nsew")
levelup_checkbutton.select()

levelup_label = Label(root, text = "Custom Levelup", height = 2, width = 12, padx = 4)
levelup_label.grid(row = 2, column = 4, sticky="nsew")

levelup_combobox = ttk.Combobox(root, value = [], width = 18)
levelup_combobox.grid(row = 3, column = 4, sticky="new")

levelup_combobox.bind('<KeyRelease>', levelup_combobox_search)

#Evolution Selection

evolution_checkbutton = Checkbutton(root, text = 'Same as Species', variable = evolution_bool, onvalue = True, offvalue = False)
evolution_checkbutton.grid(row = 1, column = 5, sticky="nsew")
evolution_checkbutton.select()

evolution_label = Label(root, text = "Custom Evolution", height = 2, width = 12, padx = 4)
evolution_label.grid(row = 2, column = 5, sticky="nsew")


evolution_combobox = ttk.Combobox(root, width = 18)
evolution_combobox.grid(row = 3, column = 5, sticky="new")

evolution_combobox.bind('<KeyRelease>', evolution_combobox_search)

#CSV file path Selection

load_pokelist_csv_button = Button(root, text = '(Re)Load CSV', command = lambda: [user_prompt_load_CSV(poke_edit_data, 'Pokemon Names and Files'), update_non_model_lists(poke_edit_data), update_model_list_for_box(poke_edit_data)], height = 2, width = 18, pady = 5, padx = 7)
load_pokelist_csv_button.grid(row = 0, column = 6, sticky="ew")

save_pokelist_csv_button = Button(root, text = 'Create/Save CSV', command = lambda: [user_prompt_write_CSV(poke_edit_data, 'Pokemon Names and Files'), update_non_model_lists(poke_edit_data), update_model_list_for_box(poke_edit_data)], height = 2, width = 18, pady = 5, padx = 7)
save_pokelist_csv_button.grid(row = 1, column = 6, sticky="ew")

#create_pokelist_csv_button = Button(root, text = 'Create/Reset CSV', command = lambda: [create_refresh_CSV(poke_edit_data,games_temp.get()), update_all_listboxes(poke_edit_data)], height = 2, width = 18, pady = 5, padx = 7)
#create_pokelist_csv_button.grid(row = 4, column = 6, sticky="ew")


#Number of New Formes
number_formes_label = Label(root, text = "# Formes To Add", height = 2, width = 12, padx = 4)
number_formes_label.grid(row = 2, column = 1, sticky="nsew")

number_formes_entry = Entry(root, width = 12)
number_formes_entry.grid(row = 3, column = 1, sticky="new")

#Run Insertion
execute_button = Button(root, text = 'Insert Forme(s)', command = lambda: [pre_check(poke_edit_data), update_non_model_lists(poke_edit_data), update_model_list_for_box(poke_edit_data)], height = 2, width = 12, pady = 5, padx = 7)
execute_button.grid(row = 3, column = 6, sticky="new")

skip_model_checkbutton = Checkbutton(root, text = 'Initialize Model Files', variable = skip_model_creation_bool, onvalue = False, offvalue = True)
skip_model_checkbutton.grid(row = 1, column = 1, sticky="nsew")
skip_model_checkbutton.select()

#print("help")
root.mainloop()