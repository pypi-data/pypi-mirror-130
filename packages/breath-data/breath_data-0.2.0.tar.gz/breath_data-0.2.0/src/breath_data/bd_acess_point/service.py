from __future__ import annotations

from typing import Callable, Dict, List, Union
from breath_api_interface.proxy import ServiceProxy
from breath_api_interface.queue import Queue
from breath_api_interface.service_interface import Service
from breath_api_interface.request import Request, Response

from breath_data.bd_acess_point.relational_querier import RelationalQuerier
from breath_data.bd_acess_point.graph_querier import GraphQuerier


class BDAcessPoint(Service):
	'''BReATH service for provide BD acess

		:ivar relational_querier: Handles relational (SQL) queries
		:type relational_querier: breath_data.bd_acess_point.relational_querier.RelationalQuerier

		:ivar graph_querier: Handles graph (Neo4j) queries
		:type graph_querier: breath_data.bd_acess_point.graph_querier.GraphQuerier
	'''

	def __init__(self, proxy:ServiceProxy, request_queue:Queue, global_response_queue:Queue):
		'''BDAcessPoint constructor.

			Initializes the service with the BDs.
		'''
		super().__init__(proxy, request_queue, global_response_queue, "BDAcessPoint")
		self.relational_querier = RelationalQuerier()
		self.graph_querier = GraphQuerier()
		
		self._operations : Dict[str, Callable[[BDAcessPoint, Request], Response]] = {
							"register_symptom" : self._register_symptom,
							"register_workflow": self._register_workflow,
							"is_workflow_runned": self._is_workflow_runned,
							"register_user": self._register_user,
							"get_symptoms_types" : self._get_symptoms_types,
							"register_symptom_type": self._register_symptom_type,
							"register_city": self._register_city,
							"register_patient" : self._register_patient,
							"get_casos" : self._get_casos,
							"get_temperature": self._get_temperature,
							"get_city": self._get_city,
							}

	
	def run(self) -> None:
		'''Run the service, handling BD requests.
		'''
		request = self._get_request()

		if request is None:
			return

		response : Response = request.create_response(sucess=False, response_data={"message": "Operation not available"})

		if request.operation_name in self._operations:
			response = self._operations[request.operation_name](request)

		self._send_response(response)

	def _cancel_all(self):
		self.relational_querier.cancel()
		#self.graph_querier.cancel()

	def _commit_all(self):
		self.relational_querier.commit()
		#self.graph_querier.commit()

	def _get_city(self, request:Request) -> Response:
		if "city_name" not in request.request_info:
			return request.create_response(False, {"message":"Request must have city_name."})

		city_name = request.request_info["city_name"]

		query = "SELECT * FROM Cidades WHERE Nome_municipio='{0}'".format(city_name)
		sucess, result, description = self.relational_querier.query(query)

		if not sucess:
			return request.create_response(False, {"message": "Relational Querier error."})

		response = request.create_response(True, {"data":result, "description":description})
		return response

	def _get_casos(self, request:Request) -> Response:
		
		if "city_name" not in request.request_info:
			return request.create_response(False, {"message":"Request must have city_name."})

		city_name = request.request_info["city_name"]

		query = "SELECT * FROM Casos_Dia WHERE ID_MUNICIP='{0}'".format(city_name)
		sucess, result, description = self.relational_querier.query(query)

		if not sucess:
			return request.create_response(False, {"message": "Relational Querier error."})

		response = request.create_response(True, {"data":result, "description":description})

		return response

	def _get_temperature(self, request:Request) -> Response:

		if "city_name" not in request.request_info:
			return request.create_response(False, {"message":"Request must have city_name."})

		city_name = request.request_info["city_name"]

		query = "SELECT DIA, Temp_max, Temp_min FROM Clima_Cidade WHERE Nome_municipio ='{0}'".format(city_name)

		sucess, result, description = self.relational_querier.query(query)

		if not sucess:
			return request.create_response(False, {"message": "Relational Querier error."})
	
		response = request.create_response(True, {"data":result, "description":description})

		return response

	def _register_user(self, request:Request) -> Response:

		name = None
		age = None
		gender = None

		if 'name' in request.request_info:
			name = request.request_info["name"]
		if 'age' in request.request_info:
			age = request.request_info["age"]
		if 'gender' in request.request_info:
			gender = request.request_info["gender"]
		sql_query = "INSERT INTO Users(Nome, Idade, Genero) VALUES('{0}',{1},'{2}')".format(name, age, gender)

		sucess, _, description = self.relational_querier.query(sql_query)

		if not sucess:
			return request.create_response(sucess=False, response_data={"message":"Cannot create user"})

		return request.create_response(sucess=True)

	def _register_symptom(self, request: Request) -> Response:
		
		symptom_name = None
		year = None
		month = None
		day = None

		if 'symptom_name' in request.request_info:
			symptom_name = request.request_info["symptom_name"]
		
		if 'year' in request.request_info:
			year = request.request_info["year"]
		if 'month' in request.request_info:
			month = request.request_info["month"]
		if 'day' in request.request_info:
			day = request.request_info["day"]

		if symptom_name is None:
			self._cancel_all()
			return request.create_response(sucess=False, response_data={"message": "Symptom type not found"})

		patient_id = 0 # colocamos esse valor para substituir a req no BD (teste)

		if "patient_id" in request.request_info:
			patient_id = request.request_info["patient_id"]
		else:
			user_id = request.request_info["user_id"]
			users = self._search_user(user_id)

			if users is None:
				self._cancel_all()
				return request.create_response(sucess=False, response_data={"message": "User not found"})

			patient_id = users[0]["Paciente"]
			city_id = users[0]["Cidade"]

		city = request.request_info["city"]

		city_id = city
		
		sql_query = "INSERT INTO Sintomas(Tipo, Ano, Mês, Dia, Cidade, Paciente)"
		sql_query += " VALUES(?, ?, ?, ?, ?, ?)"#.format(symptom_name, year, month, day, city_id, patient_id)
		
		sucess, symptom, description = self.relational_querier.query(sql_query, [0, symptom_name, year, month, day, city_id, patient_id])

		if not sucess:
			self._cancel_all()
			return request.create_response(sucess=False, response_data={"message":"Error while registering symptom"})

		print(symptom)
		symptom_id = symptom

		sql_query3 = "INSERT INTO PacienteSintoma(Paciente, Sintoma) VALUES(?, ?)"#.format(patient_id, symptom_id)
		sucess, _, description = self.relational_querier.query(sql_query3, [0, patient_id, symptom_id])

		if not sucess:
			self._cancel_all()
			return request.create_response(sucess=False, response_data={"message":"Cannot register patient symptom relation"})

		self._commit_all()

		return request.create_response(sucess=True)

	def _search_city(self, city:str) -> Union[List[Dict[str, str]], None]:
		#neo_query = "MATCH (t:Tipo_Sintoma {{nome: {0}}}) RETURN t".format(city)        
		#sucess, symptoms_types = self.graph_querier.query(neo_query)

		

		sql_query = "SELECT * from Clima_Casos WHERE Clima_Casos.Nome_municipio = '{0}'".format(city)
		
		sucess, cities_matched, description = self.relational_querier.query(sql_query)

		if not sucess:
			return None

		return cities_matched

	def _search_symptom_type(self, symptom_name:str) -> Union[List[Dict[str, str]], None]:
		#neo_query = "MATCH (t:Tipo_Sintoma {{nome: {0}}}) RETURN t".format(symptom_name)        
		#sucess, symptoms_types = self.graph_querier.query(neo_query)

		sql_query = "SELECT * from Sintomas WHERE Tipo = {0};".format(symptom_name)
		sucess, symptoms_types, description = self.relational_querier.query(sql_query)

		if not sucess:
			return None

		return symptoms_types

	def _search_user(self, user_id:int) -> Union[List[Dict[str, str]], None]:
		sql_query = "SELECT * FROM Users WHERE Users.id = {0}".format(user_id)
		sucess, users, description = self.relational_querier.query(sql_query)

		if not sucess:
			return None
		
		return users

	def _get_symptoms_types(self, request:Request) -> Response:
		#neo_query = "MATCH (t:Tipo_Sintoma RETURN t"
		#sucess, symptoms_types = self.graph_querier.query(neo_query)

		sql_query = "SELECT Tipo from Sintomas GROUP BY Tipo;"
		sucess, _, description = self.relational_querier.query(sql_query)

		if not sucess:
			return Response(False, {"message":"Unable to access symptoms types"})
		
		return Response(True, {"symptoms_types":sql_query})

	# onde guardariamos tipo de sintoma no relacional?
	def _register_symptom_type(self, request:Request) -> Response:
		neo_query = "CREATE ({0}:Tipo_Sintoma)".format(request.request_info["symptom_name"])
		sucess, _ = self.graph_querier.query(neo_query)



		if not sucess:
			return request.create_response(False, {"message":"Unable to register symptom type"}) 

		return request.create_response(True)

	def _register_city(self, request:Request) -> Response:
		uf = request.request_info["uf"]
		nome = request.request_info["nome"]
		cod = request.request_info["cod"]

		sql_query = "INSERT INTO Cidades(Id, Nome_municipio, UF) VALUES('{0}', '{1}', '{2}')".format(cod, nome, uf)

		sucess, _, description = self.relational_querier.query(sql_query)

		if not sucess:
			return request.create_response(False, {"message":"Unable to register city"})
		
		return request.create_response(True)


	def _get_symptoms_types(self, request:Request) -> Response:
		neo_query = "MATCH (t:Tipo_Sintoma) RETURN t"
		sucess, symptoms_types = self.graph_querier.query(neo_query)

	# Teremos banco pacientes alem do banco de usurios?
	def _register_patient(self, request:Request) -> Response:
		sex = request.request_info["sex"]

		sql_query = "INSERT INTO Pacientes(Sexo) VALUES('{0}')".format(sex)

		sucess, patient, description = self.relational_querier.query(sql_query)

		if not sucess:
			return request.create_response(False, {"message":"Unable to register patient"})
		
		return request.create_response(True, {"patient": patient[0]})

	def _register_workflow(self, request:Request) -> Response:
		name = request.request_info["workflow_name"]
		sql_query = "INSERT INTO Workflow(Nome, Executado) VALUES('{0}', 1)".format(name)

		sucess, _, description = self.relational_querier.query(sql_query)

		if not sucess:
			return request.create_response(False, {"message":"Unable to register workflow"})

		self._commit_all()
		
		return request.create_response(True)

	def _is_workflow_runned(self, request:Request) -> Response:
		name = request.request_info["workflow_name"]
		sql_query = "SELECT * FROM Workflow WHERE Workflow.Nome = '{0}'".format(name)
		sucess, workflows, description = self.relational_querier.query(sql_query)

		if sucess and len(workflows) > 0 and workflows[0][1] == 1:
			return request.create_response(True)

		return request.create_response(False)

	def _get_climate_interval(self, request:Request) -> Response:

		initial = None
		final = None

		if 'initial' in request.request_info:
			initial = request.request_info["initial"]
		if 'final' in request.request_info:
			final = request.request_info["final"]

		sql_query = "SELECT * from Climate WHERE date BETWEEN {0} AND {1} ORDER BY date;".format(initial, final)
		sucess, climates, description = self.relational_querier.query(sql_query)

		if not sucess:
			return None

		return climates
		
	def _get_climate_date(self, request:Request) -> Response:
		
		date = None

		if 'date' in request.request_info:
			date = request.request_info["date"]

		sql_query = "SELECT * from Climate WHERE date = {0} ORDER BY date;".format(date)
		sucess, climates, description = self.relational_querier.query(sql_query)

		if not sucess:
			return None

		return climates

	def _get_SRAG_interval(self, request:Request) -> Response:
		
		initial = None
		final = None

		if 'initial' in request.request_info:
			initial = request.request_info["initial"]
		if 'final' in request.request_info:
			final = request.request_info["final"]

		sql_query = "SELECT * from SRAG WHERE date BETWEEN {0} AND {1} ORDER BY date;".format(initial, final)
		sucess, diagnostics, description = self.relational_querier.query(sql_query)

		if not sucess:
			return None

		return diagnostics

	def _get_SRAG_date(self, request:Request) -> Response:
		
		date = None

		if 'date' in request.request_info:
			date = request.request_info["date"]

		sql_query = "SELECT * from SRAG WHERE date = {0} ORDER BY date;".format(date)
		sucess, diagnostics, description = self.relational_querier.query(sql_query)

		if not sucess:
			return None

		return diagnostics