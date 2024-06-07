import pandas as pd
from sqlalchemy import create_engine

def limpieza():
    pd.set_option("display.max_rows", None)

    csv_file_path1 = "archivos\\file_Datos.csv"
    csv_file_path2 = "archivos\\file_Secciones.csv"
    df_Datos = pd.read_csv(csv_file_path1, encoding="latin1")
    df_Detalles = pd.read_csv(csv_file_path2)
    df_Datos.drop("Unnamed: 8", axis=1, inplace=True)
    df_Detalles.dropna(inplace = True)

    ##### LIMPIEZA DE CSVs #####
    edificios = [] 
    for i in range(df_Detalles.shape[0]):
        if df_Detalles.iloc[i]["codigo_aula"][2:3] == "/":
            edificios.append(df_Detalles.iloc[i]["codigo_aula"][:2])
        else:
            edificios.append(df_Detalles.iloc[i]["codigo_aula"])
    df_Detalles["edificio"] = edificios

    aula_sola = [] 
    for i in range(df_Detalles.shape[0]):
        if df_Detalles.iloc[i]["codigo_aula"] != "" and df_Detalles.iloc[i]["codigo_aula"][2:3] == "/":
            aula_sola.append(df_Detalles.iloc[i]["codigo_aula"][3:])
        else:
            aula_sola.append(df_Detalles.iloc[i]["codigo_aula"])
    df_Detalles["aula"] = aula_sola

    carreras = []
    for i in range(df_Datos.shape[0]):
        cadena = df_Datos.iloc[i]["CARRERA"]
        cad1 = ""
        cad2 = ""
        cad3 = ""
        # agregar guión
        if cadena[1:2] != "-":
            cad1 = cadena[0:1] + "-" + cadena[1:]
        else: 
            cad1 = cadena
        
        # quitar 0 luego del guión
        if cad1[2:3] == "0":
            cad2 = cad1[0:2] + cad1[3:]
        else: 
            cad2 = cad1

        # quitar letra del final 
        if not cad2[-1].isnumeric():
            cad3 = cad2[0:-1]
        else: 
            cad3 = cad2
        carreras.append(cad3)

    df_Datos["CARRERA"] = carreras
    #print(df_Detalles)
    # datos_por_carrera = df_Datos.groupby("CARRERA").count()

    df_Tabla_Estudiantes = df_Datos[["CUENTA", "CARRERA"]]
    df_Tabla_Estudiantes.columns = ["cuenta", "carrera"]
    df_Tabla_Carrera = pd.read_excel("archivos\\Carreras Unitec.xlsx")
    df_Tabla_Seccion = df_Detalles
    df_Tabla_EstudiantesPorSeccion = df_Datos[["CUENTA", "SECCION"]]
    df_Tabla_EstudiantesPorSeccion.columns = ["cuenta", "seccion"]

    df_Tabla_Seccion["seccion"] = df_Tabla_Seccion["seccion"].astype(int)
    df_Tabla_Seccion["dias_habiles"] = df_Tabla_Seccion["dias_habiles"].astype(int).astype(str)

    engine = create_engine('sqlite:///instance/database.db')
    # Guardar el DataFrame en la base de datos SQLite
    df_Tabla_Estudiantes.to_sql('Estudiante', engine, index=False, if_exists='replace')
    df_Tabla_Carrera.to_sql('Carrera', engine, index=False, if_exists='replace')
    df_Tabla_Seccion.to_sql('Seccion', engine, index=False, if_exists='replace')
    df_Tabla_EstudiantesPorSeccion.to_sql('EstudiantePorSeccion', engine, index=False, if_exists='replace')
