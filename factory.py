
import time
import datetime



################################################################################
#   Groupe 13 - Scheduleur EPSI
	# KOKO Ambinintsoa Kantisambatra
	# MENDY Marie Hélène 
	# Yassine HEBBOUL
	# Amine
################################################################################
# Fonction pour le message quand lorsqu une tâche enregistre des données dans le fifo concerne
def message_register_fifo(task_name, fifo_name, date_register_data, fifo_variable):
	# Enregistrement des données dans la variable globale fifo concerne
    fifo_variable.append("Lire les données envoyé par "+ task_name +" à : " + date_register_data)
	# Message pour dire qu il y a un enregistrement dans fifo concerne
    print("\t" + task_name + " : Enregistre des données dans fifo "+ fifo_name +" à (" + date_register_data + ")")
    
# Fonction pour le message quand lorsqu une tâche lis des données dans le fifo concerne
def message_read_fifo(task_name, fifo_variable):
	# Initialisation de la variable d iteration
    iteration_variable = 0
    # Parcourir le tableau pour global_fifo_logs, afficher les données et par la suite les supprimer
    while iteration_variable < len(fifo_variable):
        # Afficher la valeur de case du tableau global_fifo
        print("\t"+ task_name + " : " + fifo_variable[iteration_variable])
        # Supprimer cette variable
        del fifo_variable[iteration_variable]
        # itérer la variable d itération
        iteration_variable = iteration_variable + 1
    # Dans le cas ou fifo n a pas de données(vide)
    if(len(fifo_variable) == 0):
         print("\t"+ task_name + " : Aucune données à lire dans FIFO")
	

    
    
class my_task():

	name = None
	priority = -1
	period = -1
	execution_time = -1
	last_deadline = -1
	last_execution_time = None


    	############################################################################
	def __init__(self, name, priority, period, execution_time, last_execution, fifo_datas_write = False, fifo_logs_write = False):

		self.name = name
		self.priority = priority
		self.period = period
		self.execution_time = execution_time
		self.last_execution_time = last_execution
		self.fifo_datas_write = fifo_datas_write
		self.fifo_logs_write = fifo_logs_write
        


    	############################################################################
	def run(self):
	# MAJ last_execution_time
		
		self.last_execution_time = datetime.datetime.now()

		print("\t" + self.name + " : Se déclenche à (" + self.last_execution_time.strftime("%H:%M:%S") + ")")
  
	# Si dans le cas ou la tache peut ecrire dans fifos datas(la tache sensor_acquisition)
		if (self.fifo_datas_write == True and  self.name == 'sensor_acquisition') :
		# Message pour dire qu il y a un enregistrement dans fifo datas et enregistrement des données
			message_register_fifo(self.name,"data", datetime.datetime.now().strftime("%H:%M:%S"), global_fifo_datas)
	# Si dans le cas ou la tache va lire les données de fifos datas(la tache motors_control)
		if (self.fifo_datas_write == False and  self.name == 'motors_control') :
		# Appel du fonction pour lire les données du fifo datas
			message_read_fifo(self.name,global_fifo_datas)
	# Si dans le cas ou la tache peut ecrire dans logs logs(la tache sensor_acquisition, motors_control, camera_analysis)
		if (self.fifo_logs_write == True and  self.name == 'sensor_acquisition' and  self.name == 'motors_control' and  self.name == 'camera_analysis') :
		# Enregistrement des données dans le fifos logs
			# Si dans le cas ou la tâche est sensor_acquisition
			if (self.name == 'sensor_acquisition'):
		# Message pour dire qu il y a un enregistrement dans fifo logs et enregistrement des données
				message_register_fifo(self.name,"logs", datetime.datetime.now().strftime("%H:%M:%S"), global_fifo_logs)
			# Si dans le cas ou la tâche est motors_control
			if (self.name == 'motors_control'):
		# Message pour dire qu il y a un enregistrement dans fifo logs et enregistrement des données
				message_register_fifo(self.name,"logs", datetime.datetime.now().strftime("%H:%M:%S"), global_fifo_logs)
			# Si dans le cas ou la tâche est camera_analysis
			if (self.name == 'camera_analysis'):
		# Message pour dire qu il y a un enregistrement dans fifo logs et enregistrement des données
				message_register_fifo(self.name,"logs", datetime.datetime.now().strftime("%H:%M:%S"), global_fifo_logs)
	# Si dans le cas ou la tache va lire les données de fifos logs(la tache transmission_system)
		if (self.fifo_logs_write == False and  self.name == 'transmission_system') :
		# Appel du fonction pour lire les données du fifo logs
			message_read_fifo(self.name,global_fifo_logs)

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
	global global_fifo_datas
	global global_fifo_logs
	global_fifo_logs = []
	global_fifo_datas = []
# Instanciation des objets tâches
	task_list = []
	task_list.append(my_task(name="motors_control", priority = 3, period = 10, execution_time = 1, last_execution = last_execution, fifo_datas_write = False, fifo_logs_write = True))
	task_list.append(my_task(name="sensor_acquisition", priority = 1, period = 10, execution_time = 1, last_execution = last_execution, fifo_datas_write = True, fifo_logs_write = True))
	task_list.append(my_task(name="transmission_system", priority = 4, period = 60, execution_time = 20, last_execution = last_execution, fifo_datas_write = False, fifo_logs_write = False))
	task_list.append(my_task(name="camera_analysis", priority = 2, period = 30, execution_time = 10, last_execution = last_execution, fifo_datas_write = False, fifo_logs_write = True))

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
   
			print("\tDeadline pour la tâche " + current_task.name + " : " + current_task_next_deadline.strftime("%H:%M:%S"))

		# Se déclenche si la durée d exec est inféreieur à 1 heure on remplacera le earliest_deadline par current_task_next_deadline
			if (current_task_next_deadline < earliest_deadline):
				earliest_deadline = current_task_next_deadline
				task_to_run = current_task


		# Start task
		task_to_run.run()