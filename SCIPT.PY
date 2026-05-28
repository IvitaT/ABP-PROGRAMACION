import datetime

import mysql.connector
db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="Pi+314159265",
    database="fibra_cba_db"
)

cursor = db.cursor()

print("Conectado a MySQL")

# OPCIONES PARA INICIAR LA CONVERSACION CON EL CLIENTE 

# Usamos una variable bandera (Flag) para controlar el ciclo
sistema_activo = True

while sistema_activo:
    # Imprimimos las opciones en la consola
    
    print("\n=========================================")
    print("     BIENVENIDO A FIBRACORD        ")
    print("=========================================")
    print("1. Registrar Alta de Servicio")
    print("2. Modificar Servicio (Cambiar Velocidad)")
    print("3. Dar de Baja Cliente")
    print("4. Salir")
    print("=========================================")
    
    # Capturamos la opción del usuario
    opcion = input("Seleccione una opción (1-4): ")
    
    # Evaluamos la opción usando condicionales
    if opcion == "1":
        print("\n--- 📝 FORMULARIO DE ALTA DE SERVICIO ---")
        
        # 1. ENTRADA DE DATOS (Incluye el nuevo campo de contacto)
        dni = input("DNI del Cliente: ").strip()
        nombre = input("Nombre: ").strip()
        apellido = input("Apellido: ").strip()
        correo = input("Correo Electrónico: ").strip()
        fecha_nacimiento = input("Fecha de Nacimiento (AAAA-MM-DD): ").strip()
        numero_contacto = input("Número de Contacto/Celular: ").strip()  # <-- NUEVO CAMPO
        
        
        print("\nPlanes de Velocidad: (1) 100MB - $12500 | (2) 300MB - $16800 | (3) 600MB - $23500 | (4) 1000MB - $31000")
        id_servicio = input("Seleccione el ID del servicio (1-4): ")
        
        print("\n📍 Ingrese el Barrio para verificar disponibilidad del servicio:")
        barrio_ingresado = input("Nombre del Barrio: ").strip().title()
        
        calle = input("Calle: ").strip()
        numero = int(input("Número: "))
        piso_dpto = input("Piso/Dpto (ENTER si es casa): ").strip()
        if piso_dpto == "":
            piso_dpto = None

        
        cursor.execute("SELECT id_barrio, estado_cobertura FROM cobertura WHERE nombre_barrio = %s", (barrio_ingresado,))
        cobertura_resultado = cursor.fetchone()
        
        if cobertura_resultado is not None and cobertura_resultado[1] == "OK":
            id_barrio = cobertura_resultado[0]
            
            # Lógica de fechas dinámicas
            hoy = datetime.now()
            f1 = hoy + timedelta(days=1)
            f2 = hoy + timedelta(days=2)
            f3 = hoy + timedelta(days=3)
            
            print("\n📅 Seleccione fecha para la visita del técnico:")
            print(f"1. {f1.strftime('%d/%m/%Y')}")
            print(f"2. {f2.strftime('%d/%m/%Y')}")
            print(f"3. {f3.strftime('%d/%m/%Y')}")
            opc_fecha = input("Seleccione opción (1-3): ")
            
            if opc_fecha == "1":
                fecha_visita = f1.strftime('%Y-%m-%d')
            elif opc_fecha == "2":
                fecha_visita = f2.strftime('%Y-%m-%d')
            else:
                fecha_visita = f3.strftime('%Y-%m-%d')
                
            try:
                # Insertamos en la tabla clientes incluyendo el teléfono
                query_cli = "INSERT INTO clientes (dni, nombre, apellido, numero_contacto, correo, fecha_nacimiento) VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(query_cli, (dni, nombre, apellido, numero_contacto, correo, fecha_nacimiento))
                
                # Insertamos en la tabla solicitudes
                query_sol = """INSERT INTO solicitudes (dni_cliente, id_barrio, id_servicio, calle, numero, piso_dpto, tipo_solicitud, fecha_visita, fecha_nacimiento) 
                               VALUES (%s, %s, %s, %s, %s, %s, 'Alta', %s, %s)"""
                cursor.execute(query_sol, (dni, id_barrio, id_servicio, calle, numero, piso_dpto, fecha_visita, fecha_nacimiento))
                
                conexion.commit()
                print("\n✅ ¡ÉXITO! Alta registrada.")
            except mysql.connector.Error as err:
                print(f"❌ Error en base de datos: {err}")
        else:
            print("\n❌ Lo sentimos, por el momento no contamos con cobertura en tu barrio.")
            
        db.commit()
        conexion.close()
        
    elif opcion == "2":
        print("\n[PROXIMAMENTE] Aquí programaremos la MODIFICACIÓN de velocidad.")
        
    elif opcion == "3":
        print("\n[PROXIMAMENTE] Aquí programaremos la BAJA del cliente.")
        
    elif opcion == "4":
        print("\nCerrando el sistema... ¡Hasta luego!")
        # Cambiamos la bandera a False para romper el ciclo while y salir
        sistema_activo = False
        
    else:
        print("\n⚠️ Opción inválida. Por favor, elija un número del 1 al 4.")

