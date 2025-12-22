import mysql.connector
from config.db_config import db_config


def otestuj_pripojeni():
    print("--- Zkouším se připojit k databázi... ---")

    try:
        connection = mysql.connector.connect(**db_config)

        if connection.is_connected():
            print("ÚSPĚCH! Jsi připojen k databázi:", db_config['database'])

            cursor = connection.cursor()

            query = "SELECT title, price FROM books;"
            cursor.execute(query)

            knihy = cursor.fetchall()

            print(f"\nNalezeno {cursor.rowcount} knih:")
            print("-" * 30)
            for kniha in knihy:
                print(f"{kniha[0]} (Cena: {kniha[1]} Kč)")

    except mysql.connector.Error as e:
        print("CHYBA: Něco se pokazilo při připojování.")
        print(f"Detail chyby: {e}")

    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("\n--- Připojení ukončeno ---")


if __name__ == "__main__":
    otestuj_pripojeni()