from flask import Flask, request #, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
app = Flask(__name__)
ma = Marshmallow(app)

# what dbms + db adapter + db_user + password + host:port + database name
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://hackathon_db_admin:password123@localhost:5432/hackathon_db_flask"

#create the database instance
db = SQLAlchemy(app)

@app.cli.command("create")
def create_tables():
    db.create_all()
    print("tables created")

@app.cli.command("seed")
def seed_tables():
    project1 = Project(
        title = 'Brisbane Traffic Solver',
        repository = 'https://github.com/traffic_team/traffic_solver', 
        description = 'description goes here...'
    )
    db.session.add(project1)

    project2 = Project(
        title = 'Sustainability coding board game',
        repository = 'https://github.com/ca_team/coding_board_game', 
        description = 'description goes here...'
    )
    db.session.add(project2)
    db.session.commit()
    print("tables seeded")

@app.cli.command('drop')
def drop_tables():
    db.drop_all()
    print("tables dropped")

class Project(db.Model):
    __tablename__ = "projects"
    
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String())
    repository = db.Column(db.String())
    description = db.Column(db.String())

class ProjectSchema(ma.Schema):
    class Meta:
        fields = ("id", "title", "repository", "description")

projects_schema = ProjectSchema(many=True)
project_schema = ProjectSchema()


@app.route('/')
def welcome():
    return "Welcome students to the hackathon!"

#@app.route('/projects', methods=["GET"])
#@app.route('/projects')
@app.get('/projects')
def get_projects():
    #prepare the query to get data SELECT * FROM PROJECTS
    stmt = db.select(Project)
    #get the data
    projects = db.session.scalars(stmt)
    #convert the db data into something readable by Python
    result = projects_schema.dump(projects)

    return result
    #return jsonify(result)

@app.get('/projects/<int:id>/')
def get_project_by_id(id):
    #prepare the query to get data SELECT * FROM PROJECTS WHERE ID = :id
    stmt = db.select(Project).filter_by(id = id)
    #get the data
    project = db.session.scalar(stmt)

    if project:
        #convert the db data into something readable by Python
        return project_schema.dump(project)
    else:
        return {'error' : f'Project not found with id {id}'}, 404

#@app.route('/projects', methods=["POST"])
@app.post('/projects')
def create_project():
   #create a project
   #print(request.json)
   project_fields = project_schema.load(request.json)
   new_project = Project(
        title = project_fields["title"],
        repository = project_fields["repository"], 
        description = project_fields["description"]
    )
   db.session.add(new_project)
   db.session.commit() 
   return project_schema.dump(new_project), 201

@app.delete('/projects/<int:id>')
def delete_project(id):
    stmt = db.select(Project).filter_by(id = id)
    project = db.session.scalar(stmt)

    if project:
        db.session.delete(project)
        db.session.commit()
        return {'message': f"Project {project.title} deleted successfully"}, 202
    else:
        return {'error': f"Project not found with id {id}"}, 404
    
# @app.put
@app.route('/projects/<int:id>', methods=["PUT", "PATCH"])
def update_project(id):
    stmt = db.select(Project).filter_by(id = id)
    project = db.session.scalar(stmt)

    if project:
        project.title = request.json.get("title") or project.title
        project.repository = request.json.get("repository") or project.repository 
        project.description = request.json.get("description") or project.description

        db.session.commit()
        return project_schema.dump(project), 202

    else:
        return {'error': f"Project not found with id {id}"}, 404