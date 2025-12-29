from dao.base_dao import BaseDao

class ReportDao(BaseDao):
    def get_stats(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM view_library_stats")
        stats = cursor.fetchall()
        cursor.close()
        conn.close()
        return stats