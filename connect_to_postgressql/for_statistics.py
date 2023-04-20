def topDiseases(conn):
    status = {
        'error': 202,
        'message': '',
        'data': []
    }
    cur = conn.cursor()
    cur.execute('''select e.nombre,e.descripcion,COUNT(e.nombre) as cantidad,  
                            rank() over(order by count(*) desc , e.nombre )
                    from enfermedad e
                    inner join consulta c
                    on e.id = c.id_enfermedad 
                    inner join paciente p 
                    on c.dpi_paciente = p.dpi
                    where p.status = 'Fallecido'
                    group by e.nombre,e.descripcion 
                    order by cantidad desc
                    LIMIT 10;''')
    rows = cur.fetchall()
    if len(rows) == 0:
        status['message'] = 'No se encontraron los datos'
        status['error'] = 404
        return status

    status['data'] = [{
        'nameDisease': row[0],
        'description': row[1],
        'countDeathCases': row[2],
        'ranking': row[3]
    } for row in rows]
    return status


def topDoctors(conn):
    status = {
        'error': 202,
        'message': '',
        'data': []
    }
    cur = conn.cursor()
    cur.execute('''SELECT rank() over(order by count(*) desc , m.nombre ) ,m.nombre, 
                    COUNT(*) AS total_pacientes_atendidos
                    FROM Medico m
                    JOIN Consulta c ON m.id = c.id_medico
                    GROUP BY m.id
                    ORDER BY total_pacientes_atendidos DESC
                    LIMIT 10;''')
    rows = cur.fetchall()
    if len(rows) == 0:
        status['message'] = 'No se encontraron los datos'
        status['error'] = 404
        return status

    status['data'] = [{
        'ranking': row[0],
        'nameDoctor': row[1],
        'countAttendedPatient': row[2]
    } for row in rows]
    return status


def topPatient(conn):
    status = {
        'error': 202,
        'message': '',
        'data': []
    }
    cur = conn.cursor()
    cur.execute('''
    select rank() over(order by count(*) desc , dpi ) , count(*), dpi, nombre
    from consulta
        inner join paciente p on p.dpi = consulta.dpi_paciente
    group by p.dpi, p.nombre
    order by count(*) desc
    limit 5''')
    rows = cur.fetchall()
    if len(rows) == 0:
        status['message'] = 'No se encontraron los datos'
        status['error'] = 404
        return status

    status['data'] = [{
        'ranking': row[0],
        'count': row[1],
        'dpiPatient': row[2],
        'namePatient': row[3]
    } for row in rows]
    return status
