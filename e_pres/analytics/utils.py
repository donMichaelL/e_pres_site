
def total_building_students(experiment):
    total_student = 0
    for floor in experiment.building.floor_set.all():
        if floor.stud_number:
            total_student += floor.stud_number
    return total_student
