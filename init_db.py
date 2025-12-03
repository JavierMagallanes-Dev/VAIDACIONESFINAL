import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

def init_database():
    """Inicializa la base de datos y crea las tablas necesarias"""
    
    # Primero conectamos sin especificar la base de datos para crearla
    connection = pymysql.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', 'root'),
        port=int(os.getenv('DB_PORT', 3306))
    )
    
    try:
        with connection.cursor() as cursor:
            # Crear la base de datos si no existe
            db_name = os.getenv('DB_NAME', 'sistema_alumnos')
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            cursor.execute(f"USE {db_name}")
            
            # Tabla de Usuarios (para autenticación)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    email VARCHAR(100),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    INDEX idx_username (username)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """)
            
            # Tabla de Alumnos
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS alumnos (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    codigo VARCHAR(20) UNIQUE NOT NULL,
                    dni VARCHAR(8) UNIQUE NOT NULL,
                    nombre VARCHAR(100) NOT NULL,
                    apellido VARCHAR(100) NOT NULL,
                    email VARCHAR(100),
                    telefono VARCHAR(15),
                    fecha_ingreso DATE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    INDEX idx_dni (dni),
                    INDEX idx_codigo (codigo),
                    INDEX idx_nombre_apellido (nombre, apellido)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """)
            
            # Tabla de Cursos
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS cursos (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    codigo_curso VARCHAR(20) UNIQUE NOT NULL,
                    nombre VARCHAR(150) NOT NULL,
                    creditos INT NOT NULL,
                    descripcion TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    INDEX idx_codigo_curso (codigo_curso)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """)
            
            # Tabla de Matrículas (relación Alumno-Curso)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS matriculas (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    alumno_id INT NOT NULL,
                    curso_id INT NOT NULL,
                    semestre VARCHAR(10) NOT NULL,
                    anio INT NOT NULL,
                    fecha_matricula TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (alumno_id) REFERENCES alumnos(id) ON DELETE CASCADE,
                    FOREIGN KEY (curso_id) REFERENCES cursos(id) ON DELETE CASCADE,
                    UNIQUE KEY unique_matricula (alumno_id, curso_id, semestre, anio),
                    INDEX idx_alumno (alumno_id),
                    INDEX idx_curso (curso_id),
                    INDEX idx_semestre_anio (semestre, anio)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """)
            
            # Tabla de Notas
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS notas (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    matricula_id INT NOT NULL,
                    tipo_evaluacion VARCHAR(50) NOT NULL,
                    nota DECIMAL(4,2) NOT NULL,
                    peso DECIMAL(3,2) DEFAULT 1.00,
                    fecha_evaluacion DATE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (matricula_id) REFERENCES matriculas(id) ON DELETE CASCADE,
                    INDEX idx_matricula (matricula_id),
                    INDEX idx_tipo_evaluacion (tipo_evaluacion),
                    CHECK (nota >= 0 AND nota <= 20),
                    CHECK (peso >= 0 AND peso <= 1)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """)
            
            connection.commit()
            print("✅ Base de datos y tablas creadas exitosamente")
            
            # Insertar usuario de prueba (password: admin123)
            # Hash generado con: hashlib.sha256('admin123'.encode()).hexdigest()
            cursor.execute("""
                INSERT IGNORE INTO usuarios (username, password_hash, email)
                VALUES ('admin', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 'admin@sistema.com')
            """)
            
            # Insertar algunos cursos de ejemplo
            cursos_ejemplo = [
                ('MAT101', 'Matemática Básica', 4, 'Curso introductorio de matemática'),
                ('FIS201', 'Física I', 5, 'Mecánica y termodinámica'),
                ('PROG301', 'Programación Avanzada', 4, 'Estructuras de datos y algoritmos'),
                ('BD401', 'Base de Datos', 4, 'Diseño y gestión de bases de datos'),
                ('WEB501', 'Desarrollo Web', 3, 'HTML, CSS, JavaScript y frameworks')
            ]
            
            for curso in cursos_ejemplo:
                cursor.execute("""
                    INSERT IGNORE INTO cursos (codigo_curso, nombre, creditos, descripcion)
                    VALUES (%s, %s, %s, %s)
                """, curso)
            
            connection.commit()
            print("✅ Datos de ejemplo insertados")
            
    except Exception as e:
        print(f"❌ Error al inicializar la base de datos: {e}")
        connection.rollback()
        raise e
    finally:
        connection.close()

if __name__ == '__main__':
    print("Iniciando configuración de base de datos...")
    init_database()
    print("✅ Configuración completada!")
