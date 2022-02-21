
import time
import datetime



################################################################################
#   Etudiant en M1 à l'EPSI
	# Nom: KOKO Ambinintsoa Kantisambatra
 	# Prenom: Ambinintsoa Kantisambatra
################################################################################
# Changer la valeur du tank
def change_value_tank(fifo_variable,value):
	# Initialisation de la variable d iteration
    iteration_variable = 0
    # Parcourir le tableau
    while iteration_variable < len(fifo_variable):
        # Supprimer cette variable
        del fifo_variable[iteration_variable]
    fifo_variable.append(value)
# Verifier si tank est full
def verif_max_tank(fifo_variable):
	# Initialisation de la variable d iteration
    iteration_variable = 0
    if(sum(fifo_variable) >= 50):
        change_value_tank(fifo_variable,50)
# Fonction pour le message quand lorsqu une tâche enregistre des données dans le fifo concerne
def stocker_gasoil(task_name, fifo_name, date_register_data, fifo_variable):
    # Enregistrement des données dans la variable globale fifo concerne
    if task_name == "pump1" or task_name == "pump2":
        if task_name == "pump1":
            fifo_variable.append(10)
            verif_max_tank(fifo_variable)
            # Message pour dire qu il y a un enregistrement dans fifo concerne
            print("\t" + task_name + " : Stocke des gasoil dans "+ fifo_name +" à (" + date_register_data + ") valeur:"+ str(sum(fifo_variable)))
        else:
            fifo_variable.append(20)
            verif_max_tank(fifo_variable)
            # Message pour dire qu il y a un enregistrement dans fifo concerne
            print("\t" + task_name + " : Stocke des gasoil dans "+ fifo_name +" à (" + date_register_data + ") valeur:"+ str(sum(fifo_variable)))
	
    
# Fonction pour le message quand lorsqu une tâche lis des données dans le fifo concerne
def recuperer_gasoil(task_name, fifo_variable):
    # Si machine 1 ou 2
    if task_name == "Machine1" or task_name == "Machine2":
        if task_name == "Machine1":
            gasoil_in_tank = sum(fifo_variable) - 25
            print("\t" + task_name + " : Recuperer du gasoil dans "+ fifo_name +" à (" + date_register_data + ") Construit un moteur")
            change_value_tank(fifo_variable,gasoil_in_tank)
            global_stock_motors.append(1)
            
        else:
            gasoil_in_tank = sum(fifo_variable) - 5
            print("\t" + task_name + " : Recuperer du gasoil dans "+ fifo_name +" à (" + date_register_data + ") Construit une pneu")
            global_stock_wheels.append(1)
            change_value_tank(fifo_variable,gasoil_in_tank)
	

    
    
class my_task():

	name = None
	priority = -1
	period = -1
	execution_time = -1
	last_deadline = -1
	last_execution_time = None


    	############################################################################
	def __init__(self, name, priority, period, execution_time, last_execution):

		self.name = name
		self.priority = priority
		self.period = period
		self.execution_time = execution_time
		self.last_execution_time = last_execution
        


    	############################################################################
	def run(self):
	# MAJ last_execution_time
		
		self.last_execution_time = datetime.datetime.now()

		print("\t" + self.name + " : Se déclenche à (" + self.last_execution_time.strftime("%H:%M:%S") + ")")
    # Si dans le cas ou le tank est full
	# Si dans le cas ou la tache est pump1 ou pump2
		if (self.name == 'pump2' or self.name == 'pump1') :
		# On va lancer la fonction pour stocker  du gasoil
			stocker_gasoil(self.name,"tank", datetime.datetime.now().strftime("%H:%M:%S"), global_tank)
	# Si dans le cas ou la tache est pump1 ou pump2
		if (self.name == 'Machine1' or self.name == 'Machine2') :
		# On va lancer la fonction pour recuperer du gasoil
			recuperer_gasoil(self.name,"tank", datetime.datetime.now().strftime("%H:%M:%S"), global_tank)

		time.sleep(self.execution_time)
		print("\t" + self.name + " : S'arrête à  (" + self.last_execution_time.strftime("%H:%M:%S") + ")")
			
		



####################################################################################################
#
#
#
####################################################################################################
if __name__ == '__main__':


	last_execution = datetime.datetime.now()
	
# La variable global du fifo datas et fifo logs
	global global_tank
	global global_stock_wheels
	global global_stock_motors
	global_stock_wheels = []
	global_tank = []
	global_stock_motors = []
# Instanciation des objets tâches
	task_list = []
	task_list.append(my_task(name="pump1", priority = 1, period = 10, execution_time = 2, last_execution = last_execution))
	task_list.append(my_task(name="pump2", priority = 2, period = 10, execution_time = 2, last_execution = last_execution))
	task_list.append(my_task(name="Machine1", priority = 2, period = 10, execution_time = 2, last_execution = last_execution))
	task_list.append(my_task(name="Machine2", priority = 2, period = 10, execution_time = 2, last_execution = last_execution))

# Notre boucle de l'application
	while(1):

		time_now = datetime.datetime.now()
		
		print("\nScheduleur démarre : " + time_now.strftime("%H:%M:%S"))

		# Find the task with Earliest deadline

		task_to_run = None
		earliest_deadline = time_now + datetime.timedelta(hours=1)	# Init ... not perfect but will do the job

		for current_task in task_list:
		# Code pour les deadline afin de'arrêter les tâches
			current_task_next_deadline = current_task.last_execution_time + datetime.timedelta(seconds=current_task.period)

		# Se déclenche si la durée d exec est inférieur à 1 heure on remplacera le earliest_deadline par current_task_next_deadline
			if (current_task_next_deadline < earliest_deadline):
				earliest_deadline = current_task_next_deadline
				task_to_run = current_task


		# Start task
		task_to_run.run()