from flask import request, jsonify
from config import app, db
from models import Seccion, Carrera, Estudiante, EstudiantePorSeccion
from analisis import limpieza

@app.route('/secciones', methods=['GET'])
def get_secciones():
    secciones = Seccion.query.all()
    json_secciones = list(map(lambda seccion: seccion.to_json(), secciones))
    return jsonify({"secciones":json_secciones})

@app.route('/estudiantes', methods=['GET'])
def get_estudiantes():
    estudiantes = Estudiante.query.all()
    json_estudiantes = list(map(lambda estudiante: estudiante.to_json(), estudiantes))
    return jsonify({"estudiantes":json_estudiantes})

@app.route('/carreras', methods=['GET'])
def get_carrera():
    carreras = Carrera.query.all()
    json_carreras = list(map(lambda carrera: carrera.to_json(), carreras))
    return jsonify({"carreras":json_carreras})

@app.route('/estudiantesPorSeccion', methods=['GET'])
def get_estudiantesPorSeccion():
    estudiantesPorSeccion = EstudiantePorSeccion.query.all()
    json_estudiantesPorSeccion = list(map(lambda estudiantePorSeccion: estudiantePorSeccion.to_json(), estudiantesPorSeccion))
    return jsonify({"estudiantesPorSeccion":json_estudiantesPorSeccion})

@app.route('/clases', methods=['GET'])
def get_estudiantes_por_ubicacion():
    hora1 = request.args.get('hora1')
    hora2 = request.args.get('hora2')
    dia = request.args.get('dia')
    
    if not hora1 or not hora2 or not dia:
        return jsonify({"error": "Missing parameters"}), 400
    
    # Subquery for students in hora1
    subquery1 = db.session.query(
        EstudiantePorSeccion.cuenta,
        Seccion.edificio.label('edificio_anterior'),
        Seccion.aula.label('aula_anterior')
    ).join(Seccion, EstudiantePorSeccion.seccion == Seccion.seccion).filter(
        Seccion.hora == hora1,
        Seccion.dias_habiles.contains(dia)
    ).subquery()
    
    # Subquery for students in hora2
    subquery2 = db.session.query(
        EstudiantePorSeccion.cuenta,
        Seccion.edificio.label('edificio_nuevo'),
        Seccion.aula.label('aula_nueva')
    ).join(Seccion, EstudiantePorSeccion.seccion == Seccion.seccion).filter(
        Seccion.hora == hora2,
        Seccion.dias_habiles.contains(dia)
    ).subquery()
    
    # Join the two subqueries to find students in both times
    results = db.session.query(
        subquery1.c.edificio_anterior,
        subquery1.c.aula_anterior,
        subquery2.c.edificio_nuevo,
        subquery2.c.aula_nueva,
        db.func.count().label('estudiantes')
    ).join(
        subquery2, subquery1.c.cuenta == subquery2.c.cuenta
    ).group_by(
        subquery1.c.edificio_anterior,
        subquery1.c.aula_anterior,
        subquery2.c.edificio_nuevo,
        subquery2.c.aula_nueva
    ).all()
    
    # Format the result
    result = [
        {
            "edificio_anterior": row.edificio_anterior,
            "aula_anterior": row.aula_anterior,
            "edificio_nuevo": row.edificio_nuevo,
            "aula_nueva": row.aula_nueva,
            "estudiantes": row.estudiantes
        }
        for row in results
    ]
    
    return jsonify(result)

@app.route('/clases_edificio', methods=['GET'])
def get_estudiantes_por_ubicacion_edificio():
    hora1 = request.args.get('hora1')
    hora2 = request.args.get('hora2')
    dia = request.args.get('dia')
    
    if not hora1 or not hora2 or not dia:
        return jsonify({"error": "Missing parameters"}), 400
    
    # Subquery for students in hora1
    subquery1 = db.session.query(
        EstudiantePorSeccion.cuenta,
        Seccion.edificio.label('edificio_anterior')
    ).join(Seccion, EstudiantePorSeccion.seccion == Seccion.seccion).filter(
        Seccion.hora == hora1,
        Seccion.dias_habiles.contains(dia)
    ).subquery()
    
    # Subquery for students in hora2
    subquery2 = db.session.query(
        EstudiantePorSeccion.cuenta,
        Seccion.edificio.label('edificio_nuevo')
    ).join(Seccion, EstudiantePorSeccion.seccion == Seccion.seccion).filter(
        Seccion.hora == hora2,
        Seccion.dias_habiles.contains(dia)
    ).subquery()
    
    # Join the two subqueries to find students in both times
    results = db.session.query(
        subquery1.c.edificio_anterior,
        subquery2.c.edificio_nuevo,
        db.func.count().label('estudiantes')
    ).join(
        subquery2, subquery1.c.cuenta == subquery2.c.cuenta
    ).group_by(
        subquery1.c.edificio_anterior,
        subquery2.c.edificio_nuevo
    ).all()
    
    # Format the result
    result = [
        {
            "edificio_anterior": row.edificio_anterior,
            "edificio_nuevo": row.edificio_nuevo,
            "estudiantes": row.estudiantes
        }
        for row in results
    ]
    
    return jsonify(result)

@app.route('/estudiantes_carrera', methods=['GET'])
def get_estudiantes_por_carrera():
    hora1 = request.args.get('hora1')
    hora2 = request.args.get('hora2')
    dia = request.args.get('dia')
    carrera = request.args.get('carrera')
    
    if not hora1 or not hora2 or not dia or not carrera:
        return jsonify({"error": "Missing parameters"}), 400
    
    # Subquery for students in hora1
    subquery1 = db.session.query(
        EstudiantePorSeccion.cuenta
    ).join(Seccion, EstudiantePorSeccion.seccion == Seccion.seccion).filter(
        Seccion.hora == hora1,
        Seccion.dias_habiles.contains(dia)
    ).subquery()
    
    # Subquery for students in hora2
    subquery2 = db.session.query(
        EstudiantePorSeccion.cuenta
    ).join(Seccion, EstudiantePorSeccion.seccion == Seccion.seccion).filter(
        Seccion.hora == hora2,
        Seccion.dias_habiles.contains(dia)
    ).subquery()
    
    # Join the two subqueries to find students in both times
    results = db.session.query(
        db.func.count().label('estudiantes')
    ).filter(
        Estudiante.cuenta == EstudiantePorSeccion.cuenta,
        Estudiante.carrera == carrera
    ).scalar()
    
    return jsonify({"estudiantes": results})

@app.route('/clases_por_carrera_edificio', methods=['GET'])
def get_estudiantes_por_carrera_edificio():
    hora1 = request.args.get('hora1')
    hora2 = request.args.get('hora2')
    dia = request.args.get('dia')
    carrera = request.args.get('carrera')
    
    if not hora1 or not hora2 or not dia or not carrera:
        return jsonify({"error": "Missing parameters"}), 400
    
    # Subquery for students in hora1
    subquery1 = db.session.query(
        EstudiantePorSeccion.cuenta,
        Seccion.edificio.label('edificio_anterior')
    ).join(Seccion, EstudiantePorSeccion.seccion == Seccion.seccion).filter(
        Seccion.hora == hora1,
        Seccion.dias_habiles.contains(dia)
    ).subquery()
    
    # Subquery for students in hora2
    subquery2 = db.session.query(
        EstudiantePorSeccion.cuenta,
        Seccion.edificio.label('edificio_nuevo')
    ).join(Seccion, EstudiantePorSeccion.seccion == Seccion.seccion).filter(
        Seccion.hora == hora2,
        Seccion.dias_habiles.contains(dia)
    ).subquery()
    
    # Join the two subqueries to find students in both times
    results = db.session.query(
        subquery1.c.edificio_anterior,
        subquery2.c.edificio_nuevo,
        db.func.count().label('estudiantes')
    ).join(
        subquery2, subquery1.c.cuenta == subquery2.c.cuenta
    ).join(
        Estudiante, EstudiantePorSeccion.cuenta == Estudiante.cuenta
    ).filter(
        Estudiante.carrera == carrera
    ).group_by(
        subquery1.c.edificio_anterior,
        subquery2.c.edificio_nuevo
    ).all()
    
    # Format the result
    result = [
        {
            "edificio_anterior": row.edificio_anterior,
            "edificio_nuevo": row.edificio_nuevo,
            "estudiantes": row.estudiantes
        }
        for row in results
    ]
    
    return jsonify(result)

@app.route('/cargar', methods=['POST'])
def cargarArchivo():
    try: 
        #path_datos = request.files['fileDatos']
        #path_detalles = request.files['fileSecciones']
        #path_datos.save('archivos/file_Datos.csv')
        #path_detalles.save('archivos/file_Secciones.csv')
        datos = request.files['fileDatos']
        detalles = request.files['fileSecciones']
        limpieza(datos, detalles)
        return jsonify({'message': 'Function executed successfully'}), 200
    except Exception as e:
        print("Error:", e)
        return jsonify({'error': str(e)}), 400

