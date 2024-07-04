import pandas as pd

def allocate_rooms(group_filepath, hostel_filepath):
    group_df = pd.read_csv(group_filepath)
    hostel_df = pd.read_csv(hostel_filepath)
    
    allocation = []
    
    group_df = group_df.sort_values(by='Members', ascending=False)
    hostel_df = hostel_df.sort_values(by='Capacity', ascending=False)
    
    remaining_capacity = {row['Hostel Name'] + ' ' + str(row['Room Number']): row['Capacity'] for idx, row in hostel_df.iterrows()}
    
    for idx, group in group_df.iterrows():
        group_id = group['Group ID']
        members = group['Members']
        gender = group['Gender']
        
        for h_idx, hostel in hostel_df.iterrows():
            hostel_name = hostel['Hostel Name']
            room_number = hostel['Room Number']
            capacity = hostel['Capacity']
            hostel_gender = hostel['Gender']
            
            if gender == hostel_gender and members <= remaining_capacity[hostel_name + ' ' + str(room_number)]:
                allocation.append([group_id, hostel_name, room_number, members])
                remaining_capacity[hostel_name + ' ' + str(room_number)] -= members
                break
    
    allocation_df = pd.DataFrame(allocation, columns=['Group ID', 'Hostel Name', 'Room Number', 'Members Allocated'])
    return allocation_df
