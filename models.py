from config import db

class Seccion(db.Model):
    __tablename__ = 'Seccion'
    
    seccion = db.Column(db.Integer, primary_key=True, unique=True)
    codigo_materia = db.Column(db.String(6), nullable=False)
    hora = db.Column(db.String(10), nullable=False)
    edificio = db.Column(db.String(5), nullable=False)
    aula = db.Column(db.String(5), nullable=False)
    dias_habiles = db.Column(db.String(10), nullable=False)
    
    def to_json(self):
        return {
            "seccion": self.seccion,
            "codigo_materia": self.codigo_materia,
            "hora": self.hora,
            "edificio": self.edificio,
            "aula": self.aula,
            "diasHabiles": self.dias_habiles,
        }

class Carrera(db.Model):
    __tablename__ = 'Carrera'
    
    codigo = db.Column(db.String(4), unique=True, primary_key=True)
    nombre = db.Column(db.String(20), nullable=False)
    facultad = db.Column(db.String(100), nullable = False)
    
    def to_json(self):
        return {
            "codigo": self.codigo,
            "nombre": self.nombre,
            "facultad": self.facultad
        }

class Estudiante(db.Model):
    __tablename__ = 'Estudiante'
    
    cuenta = db.Column(db.String(8), nullable=False, primary_key=True)
    carrera = db.Column(db.String(4), db.ForeignKey('carrera'), nullable=False)
    #carrera = db.relationship('Carrera', backref=db.backref('estudiantes', lazy=True))
    
    def to_json(self):
        return {
            "cuenta": self.cuenta,
            "carrera": self.carrera,
        }
        

class EstudiantePorSeccion(db.Model):
    __tablename__ = 'EstudiantePorSeccion'
    
    cuenta = db.Column(db.String(8), nullable=False, primary_key=True)
    seccion = db.Column(db.Integer, primary_key=True, unique=True)
    #carrera = db.relationship('Carrera', backref=db.backref('estudiantes', lazy=True))
    
    def to_json(self):
        return {
            "cuenta": self.cuenta,
            "seccion": self.seccion,
        }