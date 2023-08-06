from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sro_db.model.stakeholder.models import *
from sro_db.model.organization.models import ScrumTeam, DevelopmentTeam
from sro_db.model.process.models import ScrumProject
from sro_db.model.organization.models import Organization
from sro_db.service.core.service import ApplicationReferenceService
from sro_db.service.base_service import BaseService
from pprint import pprint
class PersonService(BaseService):

    def __init__(self):
        super(PersonService,self).__init__(Person)
    
    def get_all(self, organization_uuid):
        return self.session.query(self.object).join(Organization).filter(Organization.uuid == organization_uuid).order_by(self.object.id)
    
    def get_by_email(self, email):
        return self.session.query(self.object).filter(Person.email == email).first()

class TeamMemberService(BaseService):
    def __init__(self):
        super(TeamMemberService,self).__init__(TeamMember)
        
    def retrive_by_external_id_and_project_name (self, person, project_name):
        with self.create_session_connection() as session: 
            print("Existe o projeto?")  
            scrum_team = session.query(ScrumTeam).join(ScrumProject).filter(ScrumProject.name.like (project_name)).first()
            if scrum_team is None:
                return None
            developmen_team = session.query(DevelopmentTeam).filter(DevelopmentTeam.scrum_team_id == scrum_team.id).first()
            
            print("Existe a equipe e a pessoa? ")
            print(f"Equipe: {developmen_team.id}")
            print(f"Pessoa(name id): {person.name} {person.id}")
            if developmen_team is not None and person is not None: 
                result = session.query(TeamMember).join(DevelopmentTeam).filter(TeamMember.team_id == developmen_team.id, TeamMember.person_id == person.id).first()
                return result
            
            return None

class DeveloperService(BaseService):
    def __init__(self):
        super(DeveloperService,self).__init__(Developer)
    
    def create_with_project_name(self, person, project_name):
        
        scrum_team = self.session.query(ScrumTeam).join(ScrumProject).filter(ScrumProject.name.like (project_name)).first()
        developmen_team = self.session.query(DevelopmentTeam).filter(DevelopmentTeam.scrum_team_id == scrum_team.id).first()

        developer = Developer()
        developer.name = person.name
        developer.description = person.description
        developer.person_id = person
        developer.team_role = ""
        developer.team_id = developmen_team
        return developer

    
class ScrumMasterService(BaseService):
    def __init__(self):
        super(ScrumMasterService,self).__init__(ScrumMaster)

class ProductOwnerService(BaseService):
    def __init__(self):
        super(ProductOwnerService,self).__init__(ProductOwner)

class ClientService(BaseService):
    def __init__(self):
        super(ClientService,self).__init__(Client)