from database.DB_connect import DBConnect
from model.state import State


class DAO():

    @staticmethod
    def getAnni():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select distinct extract(year from datetime) as anno
                    from sighting"""

        cursor.execute(query,)
        for row in cursor:
            result.append(row['anno'])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getForme():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select distinct s.shape 
                    from sighting s"""

        cursor.execute(query, )
        for row in cursor:
            result.append(row['shape'])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getNodes():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select *
                    from state s"""

        cursor.execute(query, )
        for row in cursor:
            result.append(State(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getEdge(forma, anno, idMap):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select state1, state2, count(*) as N
                    from neighbor n, sighting s 
                    where s.shape = %s and extract(year from s.`datetime`) = %s
                    and n.state1 < n.state2 and (upper(s.state) = state1 or upper(s.state) = state2)
                    group by state1, state2"""

        cursor.execute(query, (forma, anno,))
        for row in cursor:
            result.append((idMap[row['state1']],
                           idMap[row['state2']],
                           row['N']))

        cursor.close()
        conn.close()
        return result
