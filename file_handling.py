import shutil
import mmap
import os
import shutil

from utilities import *
from my_constants import *
    
#updated target Personal file with new Forme Count and First Forme Pointer
def personal_file_update(poke_edit_data, target_index, total_formes, start_location):
    #open target personal file
    with open(file_namer(poke_edit_data.personal_path, target_index, poke_edit_data.personal_filename_length, poke_edit_data), "r+b") as f:
        with mmap.mmap(f.fileno(), length=0, access=mmap.ACCESS_WRITE) as personal_hex_map:
            personal_hex_map.flush()
            #print('about to write ', new_forme_count)
            
            #set these two edits to only write if they are bigger than 0, allows this function to be called and only update one of them
            if(total_formes > 0):
                personal_hex_map[0x20] = total_formes
            if(start_location > 0):    
                personal_hex_map[0x1C], personal_hex_map[0x1D] = little_endian_chunks(start_location)
            
                personal_hex_map.flush()
    return(poke_edit_data)
            
#rebuilds personal compilation file
def concatenate_bin_files(folder_path):

    #generation = 7
    pad_count = 4
    #max_binary_file = 9999
    
    
    #grab list of filenames inside folder
    dir_list = os.listdir(folder_path)
    
    #check to see gen. Gen 6 has 3 char, 7 has 4, with extension is 7 and 8
    if(len(dir_list[0]) == 8):
        #generation = 7
        pad_count = 4
        #max_binary_file = 9999
    elif(len(dir_list[0]) == 7):
        #generation = 6
        pad_count = 3
        #max_binary_file = 999
    else:
        print("Error with filename")
        return
    #check to see if current directory has the compilation file:
    #grab last index
    
    #if length of last element is greater than dec 84, is compilation file (or something is wrong)
    if(os.path.getsize(os.path.join(folder_path, dir_list[-1])) > 84):
        # move the old compilation file to current directory and stick "backup_" in front of it
        os.rename(os.path.join(folder_path, dir_list[-1]), 'backup_' + dir_list[-1])
        print('Backed up old compilation file to executable\'s directory')
        
        #remove compilation file from dir_list
        del dir_list[-1]
    
    #print(len(dir_list)-1, " Pokemon entries detected.")
    
    with open(os.path.join(folder_path, str(len(dir_list)).zfill(pad_count) + '.bin'), 'wb') as output_stream:
        for file_name in dir_list:
            file_path = os.path.join(folder_path, file_name)
            
            if os.path.exists(file_path):
                with open(file_path, 'rb') as file:
                    data = file.read()
                    output_stream.write(data)
    print('New compilation file created')
    
    return


def update_model_csv_after_insert(poke_edit_data, base_form_index, new_forme_count, start_location, old_model_table = [], first_byte = 0x0, second_byte = 0x0):
    

    #get all row numbers of this species
    working_indices = find_rows_with_column_matching(poke_edit_data.master_list_csv, 2, int(base_form_index))
    
    #grab the base species name since we'll be using that at least once
    base_species_name = poke_edit_data.master_list_csv[working_indices[0]][0]
    
    #and the last model index number (as we inserted the models after that)
    #model_index_start = poke_edit_data.master_list_csv[working_indices[-1]][4]
    
    #index we start inserting the new rows from
    csv_insertion_point = max(working_indices) + 1

    #Second, we insert the new rows
    #base species index, personal file index, model index, species name, forme name
    for offset in range(new_forme_count):
        #note that model index is set to zero, since we will do one big sweep after this to update all that come after, anyway
        #Forme name is set to the number alt forme it is (e.g. if we add a forme to a Pokemon with 3 existing alt formes, it will be 4 (as the base species itself is 0))
        poke_edit_data.master_list_csv.insert(csv_insertion_point + offset, [base_species_name, len(working_indices) + offset, base_form_index, start_location + offset, 0])
        if(old_model_table != []):
            #csv has 1 extra row for the personal entry, so we need to insert 1 earlier than the csv
            #using variables with default value to allow possible future compatability with different model reference types
            old_model_table.insert(csv_insertion_point - 1 + offset, [first_byte,second_byte])
            

    #modelless_skip_count = 0
    #third we sweep through the entire array and update the model numbers, starting from the first newly inserted row
    for offset in range(1, len(poke_edit_data.master_list_csv)):
        poke_edit_data.master_list_csv[offset][4] = offset - 1 #- modelless_skip_count
        
    return(poke_edit_data, old_model_table)

def update_model_list(poke_edit_data):
    
    #if we haven't loaded the Personal file yet, we will need to do all the rest later
    if(len(poke_edit_data.personal) == 0):
        poke_edit_data.run_model_later = True
        print('Will initialize Model list after the Personal list')
        return
    else:
        poke_edit_data.run_model_later = False
        print('Initializing default Model list')
    model_temp_list = []
    with open(file_namer(poke_edit_data.model_path, 0, poke_edit_data.model_filename_length, poke_edit_data), "r+b") as f:
        with mmap.mmap(f.fileno(), length=0, access=mmap.ACCESS_READ) as model_hex_map:
            
            #for base formes plus egg at poke_edit_data.max_species_index
            for index in range(poke_edit_data.max_species_index):
                #number of model sets this species has
                number_of_models = int(model_hex_map[(index)*4 + 2])
              
                #grab the name
                temp_name = poke_edit_data.base_species_list[index + 1]
                
                #name each model as <Pokemon species> <number>, the base forme is named <Pokemon> 0 so that (in at least most cases) the model-number lines up with the forme-number (where there are multiple)
                for distinct_models in range(0, number_of_models):
                    model_temp_list.append(temp_name + ' ' + str(distinct_models))
    
    #append the Egg
    model_temp_list.append('Egg')

    #copy this into the current list to initialize properly (particularly when loading from cfg)
    poke_edit_data.model_source_list = model_temp_list.copy()                
    poke_edit_data.current_model_source_list = poke_edit_data.model_source_list.copy()

    return(poke_edit_data)

'''def conditional_update_modelless_formes_list(poke_edit_data):
    if(poke_edit_data.modelless_formes == []):
        match poke_edit_data.game:
            case "XY":
                poke_edit_data.modelless_formes = xy_modelless_formes
            case "ORAS":
                poke_edit_data.modelless_formes = oras_modelless_formes
            case "SM":
                poke_edit_data.modelless_formes = sm_modelless_formes
            case "USUM":
                poke_edit_data.modelless_formes = usum_modelless_formes
    return(poke_edit_data)'''

#adds missing models (e.g. Dusk Rockruff or from incomplete manual forme insertion)
def add_missing_models(poke_edit_data):
    #locate base species with missing models
    personal_forme_count = []
    species_has_unique_personal_genders_array = []
    temp_master = []
    #grab the current game's default list:


    for species_index in range(1, poke_edit_data.max_species_index + 1):
        
        #build array with the jth element being the j+1th species' personal forme count
        with open(file_namer(poke_edit_data.personal_path, species_index, poke_edit_data.personal_filename_length, poke_edit_data), "r+b") as f:
            with mmap.mmap(f.fileno(), length=0, access=mmap.ACCESS_WRITE) as personal_hex_map:
                    #if the forme pointer bytes are 0x0000, then there is only the single Personal file    
                    if(personal_hex_map[0x1C] != 0x0 or personal_hex_map[0x1D] != 0x0):
                        personal_forme_count.append(personal_hex_map[0x20])
                        #check to see what the gender byte in the next personal file is
                        with open(file_namer(poke_edit_data.personal_path, int(str(personal_hex_map[0x1C] + personal_hex_map[0x1D]*256)), poke_edit_data.personal_filename_length, poke_edit_data), "r+b") as f_1:
                            with mmap.mmap(f_1.fileno(), length=0, access=mmap.ACCESS_WRITE) as personal_hex_map_1:
                                
                                #if they have the same gender value, then not unique gendered formes (at most cosmetic). Also, if one of them is not all-male or all female, then something else, like Pikachu (base is 50/50, first personal forme is 100% male, but has alt female model for regular)
                                if(personal_hex_map_1[0x12] == personal_hex_map[0x12] or not (personal_hex_map[0x12] in {0x0, 0xFE} and personal_hex_map_1[0x12] in {0x0, 0xFE})):
                                    species_has_unique_personal_genders_array.append(False)
                                else:
                                    species_has_unique_personal_genders_array.append(True)
                    else:
                        personal_forme_count.append(0x1)
                        species_has_unique_personal_genders_array.append(False)
        #print(str(species_index), species_has_unique_personal_genders_array[species_index - 1])
                        
    #print(personal_forme_count)
    with open(file_namer(poke_edit_data.model_path, 0, poke_edit_data.model_filename_length, poke_edit_data), "r+b") as f:
        with mmap.mmap(f.fileno(), length=0, access=mmap.ACCESS_WRITE) as model_hex_map:
            model_hex_map.flush()
            
            #look for species with fewer formes than personal files. This 
            for species_index, current_personal_forme_count in reversed(list(enumerate(personal_forme_count))):
                
                #if this species has a gender-difference forme, subtract one from the model count (this detects if, for example, we added Mega Venusar Y but no model, because then we have 3 personal files (base, original Mega, and Y) and 3 model files (base male, base female, original mega), but only if the total formes is more than in the stock game
                #It might be possible to add more than 1 gender difference forme (e.g. have Mega Venusaur have alt female mega forme), if we verify will figure out how to find that out from this table
                total_personal_models = model_hex_map[4*species_index + 2]
                    
                
                '''
                    cases
                    1) More Models than Personal. Don't care
                    2) More Personal than Model. Only should happen from manual insert or something like Rockruff. Either way need to insert Personal - Model (from GARC) models and update the master list. This will always run after the thing that rebuilds the CSV to have the right number of rows
                    3) Need to account for gender-difference models. Check the relevant bit to see if there is a female forme. In that case the base form has 1 personal for 2 models OR 2 for 2 (Meowstic). this gives amount_to_add < 0, which is fine if nothing else.
                        We can check for this by looking at the gender of the first two personal files, if it's All Male/All Female, then meowstic case (proceed as normal, but DON'T update the bitflag at the end to have alt formes be true). Otherwise, the gender difference is cosmetic, we should update the flag, and we have 1 extra model
                '''
                
                #like Meowstic, alt-gender has unique personal. No extra models.
                if(species_has_unique_personal_genders_array[species_index]):
                    amount_to_add = current_personal_forme_count - total_personal_models - 1
                #otherwise, if the "gendered forme model" bit is 1, then we have an extra model
                elif(model_hex_map[4*species_index + 3] >> 1 & 1):
                    amount_to_add = current_personal_forme_count - (total_personal_models - 1)
                #otherwise no gendered formes at all
                else:
                    amount_to_add = current_personal_forme_count - total_personal_models

                
                #print(real_personal_count, real_model_count, stock_model_exceeds_personal, amount_to_add, current_personal_forme_count, total_personal_models)
                if(amount_to_add > 0):
                    #print(amount_to_add, poke_edit_data.base_species_list[species_index +1], current_personal_forme_count, total_personal_models)
                    
                    #updated_species.append(species_index+1)
                    new_forme_count = amount_to_add
                    #number of models on pokemon getting new forms + total number of models of all prior Pokemon
                    total_previous_models = model_hex_map[4*(species_index) + 2] + model_hex_map[4*(species_index) + 1]*256 + model_hex_map[4*(species_index) + 0]
                
                    model_source_index = model_hex_map[4*(species_index) + 1]*256 + model_hex_map[4*(species_index) + 0]
            
                    #this is the model we're copying
                    model_start_file = 0
                    #this is where we have to insert those copies after
                    model_dest_file = 0
                    #this is how many of those files there are per new forme
                    model_file_count = 0
            
                    if(poke_edit_data.game == 'XY'):
                        model_start_file = 8*(model_source_index)+3+1
                        model_dest_file = 8*total_previous_models+3
                        model_file_count = 8
                    elif(poke_edit_data.game == "ORAS"):
                        model_start_file = 8*(model_source_index)+2+1
                        model_dest_file = 8*total_previous_models+2
                        model_file_count = 8
                    #assume SM or USUM
                    else:
                        model_start_file = 9*(model_source_index)+1
                        model_dest_file = 9*total_previous_models
                        model_file_count = 9
            
                    print("Shifting model files for species after index", str(species_index + 1), ' ', poke_edit_data.base_species_list[species_index +1])

                    #shift the later model files forward
                    for file_number, file in reversed(list(enumerate(poke_edit_data.model))):
                        #if we've hit the *last* file of the Pokemon we're adding forme(s) too, stop this
                        if(file_number == model_dest_file):
                            break
                        #move file (# files per model)*(# new formes added) numbers forward
                        os.rename(file_namer(poke_edit_data.model_path, file_number, poke_edit_data.model_filename_length, poke_edit_data, poke_edit_data.model_folder_prefix), file_namer(poke_edit_data.model_path, file_number + model_file_count*new_forme_count, poke_edit_data.model_filename_length, poke_edit_data, poke_edit_data.model_folder_prefix))
                        
                        #print(file_namer(poke_edit_data.model_path, file_number, poke_edit_data.model_filename_length, poke_edit_data), ' ', file_namer(poke_edit_data.model_path, file_number + model_file_count*new_forme_count, poke_edit_data.model_filename_length, poke_edit_data))
                       
                        #update the model file list. Otherwise if we do more than 1 forme it will miss the last files and crash
                        poke_edit_data.model.append(file_number + model_file_count*new_forme_count)
                    #print(model_start_file, model_dest_file)
                    #copies each of the source model/texture/animation files from A.bin to the filename cleared up by the previous for loop
                        
                    for x in range(0, new_forme_count):
                        for y in range(0, model_file_count):
                            shutil.copy(file_namer(poke_edit_data.model_path, model_start_file + y, poke_edit_data.model_filename_length, poke_edit_data, poke_edit_data.model_folder_prefix), file_namer(poke_edit_data.model_path, model_dest_file + x*model_file_count + y + 1, poke_edit_data.model_filename_length, poke_edit_data, poke_edit_data.model_folder_prefix))

                    #reset the model filename list, since we added stuff to the end
                    poke_edit_data.model = []
                    for filename in os.listdir(poke_edit_data.model_path):
                        filename_stripped, ext = os.path.splitext(filename)
                        poke_edit_data.model.append(filename_stripped)
                    #print(len(poke_edit_data.model))
                    #print("New model files initialized for species index", str(species_index + 1))
                    #print("Updating model header for species index", str(species_index + 1))
            
                    #Now need to update model header
            
                    #set the non-gendered form bit to true if not so set, unless the Pokemon has unique personal for its alt gender
                    if(model_hex_map[4*(species_index) + 3] < 0x05 and not(species_has_unique_personal_genders_array[species_index])):
                        model_hex_map[4*(species_index) + 3] += 0x04
            
            
                    #update the number of models for the species
                    model_hex_map[4*(species_index) + 2] += new_forme_count
            
            
                    #update the "model count so far" value
                    #poke_edit_data.max_species_index + 1 because egg is last at position poke_edit_data.max_species_index (0 is Bulba, poke_edit_data.max_species_index - 1 is the last species in nat dex)
                    #because for loop, would need to subtract 1 (0,poke_edit_data.max_species_index - 1) normally, but +1 for egg
            
                    #grab model count so far
                    model_count = 0
            
                    #update number of models
                    #start from the beginning just in case something erred at another point
                    for index in range(0, poke_edit_data.max_species_index):
                        model_hex_map[4*index + 0], model_hex_map[4*index + 1] = little_endian_chunks(model_count)
                        model_count += model_hex_map[4*index + 2]
             
                    #after the first part of the file, the next part (starting immediately after the last four bytes of the above described section of the model table header that mark the Egg model) has 2 bytes per *model*, the values of which have some pattern but make about no sense at all. Perhaps legacy data? In any event the game needs there be those 2 bytes per model, so the following section shifts this table forward by the appropriate amount to insert 00 00 for each new model added (not adding them to the end just in case something somehow needs those in the expected spot).
                    #This section starts at poke_edit_data.max_species_index*4
                    
            
                    #number of bytes to move
                    #this is the length (in bytes) of the entire table, minus 4*(poke_edit_data.max_species_index+1) (to include the Egg), minus the number of models before the spot we're inserting into:
                    length_of_bytes_to_move = len(model_hex_map) - (poke_edit_data.max_species_index+1)*4 - total_previous_models*2
            
                    #add 2*<number formes added> bytes to the model table
                    model_hex_map.resize(len(model_hex_map) + 2*new_forme_count)
            
                    #move(dest, src, cont) - moves the cont bytes starting at src to dest (note destination is just source plus twice as many bytes as models inserted)
                    model_hex_map.move(poke_edit_data.max_species_index*4 + total_previous_models*2 + 2*new_forme_count, poke_edit_data.max_species_index*4 + total_previous_models*2, length_of_bytes_to_move)
            
                    #set the bytes for the new models to 0x00
                    for offset in range(0, 2*new_forme_count):
                        model_hex_map[poke_edit_data.max_species_index*4 + total_previous_models*2 + offset] = 0x00
                    print('Model header updated for species index', str(species_index + 1))

    #print('Missing formes initialized!' + '\n')

    #Now update the csv table. All we did was add model files for what's there, so all we have to do is start at the 2nd row and add 1 the model index every time we go forwards
    for row_number, row in enumerate(poke_edit_data.master_list_csv):
        if(row_number != 0):
            row[4] = row_number - 1
    
    #no formes should be without model now:
    poke_edit_data.modelless_exists = False
   # print('Internal tables updated with changes' + '\n' + '\n')
    

    return(poke_edit_data)

def update_species_list(poke_edit_data, overwrite_from_default = False):
    
    if(overwrite_from_default or (len(poke_edit_data.master_list_csv) < 100)):
        print('Initializing default Species list')
        #set base species list based on which game we're dealing with
        #grab the species name from the master list
        if(poke_edit_data.game == "USUM"):
            poke_edit_data.master_list_csv = usum_master_list_csv.copy()
            poke_edit_data.base_species_list = entire_of_column(usum_master_list_csv, 0, False)
        if(poke_edit_data.game == "SM"):
            poke_edit_data.master_list_csv = sm_master_list_csv.copy()
            poke_edit_data.base_species_list = entire_of_column(sm_master_list_csv, 0, False)
        elif(poke_edit_data.game == "XY" or poke_edit_data.game == "ORAS"):
            poke_edit_data.master_list_csv = xy_master_list_csv.copy()
            poke_edit_data.base_species_list = entire_of_column(xy_master_list_csv, 0, False)
    else:
        poke_edit_data.base_species_list = entire_of_column(poke_edit_data.master_list_csv, 0, False)
        
    #remove the model-only Egg from the end:
    poke_edit_data.base_species_list.pop() 

    #first part of master formes list is just the base species list
    poke_edit_data.master_formes_list = poke_edit_data.base_species_list.copy()
    
    #add appropriate number of spots
    #first find total number of files, then don't count the compilation file
    try:
        temp_size = os.path.getsize(file_namer(poke_edit_data.personal_path, poke_edit_data.personal[-1], poke_edit_data.personal_filename_length, poke_edit_data))
        if(temp_size > 84):
            personal_index_count = len(poke_edit_data.personal) - 1
        else:
            personal_index_count = len(poke_edit_data.personal)
    #if that doesn't exist, we don't count it either
    except:
            personal_index_count = len(poke_edit_data.personal) - 1
        
    print("Initializing default Formes list")
    #adds (total number of pokemon personal files) - (total number of base species) spots to the end of the array
    for x in range(0, personal_index_count - poke_edit_data.max_species_index - 1):
        poke_edit_data.master_formes_list.append('')
        

    #print(poke_edit_data.max_species_index)
    #open personal
    #open each file until max species, note pointer and forme count
    #reference hardcoded list to spit out <species> <number> like pk3ds
    #iterate through the personal files
    for index, file in enumerate(poke_edit_data.personal):
        #since we're filling up the poke_edit_data.master_formes_list by iterating through the base formes, we can stop when we finish the last base Pokemon
        #poke_edit_data.max_species_index is here the first alt forme because off-by-1, so stop here
        if(index == poke_edit_data.max_species_index + 1):
            break
        

        with open(file_namer(poke_edit_data.personal_path, file, poke_edit_data.personal_filename_length, poke_edit_data), "r+b") as f:
            with mmap.mmap(f.fileno(), length=0, access=mmap.ACCESS_READ) as personal_hex_map:
                #pull # of formes
                forme_count = personal_hex_map[0x20]
                forme_pointer = personal_hex_map[0x1C] + 256*personal_hex_map[0x1D]
                #if more than 1 AND forme pointer not 0, need to update those names in the array
                if(forme_count > 1 and forme_pointer != 0):
                    #this is the internal index number of the first alt forme, less 1 because we're shifted over one
                    
                    #print(index, forme_count, forme_pointer)
                    #first forme in forme count is the base, need to do 1 less than that. We call each forme <base species name> <alt forme count> (e.g. Mega Blastoise is "Blastoise 1")
                    for x in range(0, forme_count - 1):
                        #print(index, forme_count, forme_pointer, x)
                        poke_edit_data.master_formes_list[forme_pointer + x] = poke_edit_data.base_species_list[index] + ' ' + str(x+1)
    #print(poke_edit_data.master_formes_list)
    #if we loaded Model before Personal, need to load Model now
    if(poke_edit_data.run_model_later):
        poke_edit_data = update_model_list(poke_edit_data)
        
    #copy this into the current list to initialize properly (particularly when loading from cfg)
    poke_edit_data.current_base_species_list = poke_edit_data.base_species_list.copy()
    poke_edit_data.current_personal_list = poke_edit_data.master_formes_list.copy()
    poke_edit_data.current_levelup_list = poke_edit_data.master_formes_list.copy()
    poke_edit_data.current_evolution_list = poke_edit_data.master_formes_list.copy()
    
    return(poke_edit_data)
