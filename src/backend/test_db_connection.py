from sqlmodel import Session, create_engine, text, select
from app.core.config import settings

def test_db_connection():
    
    try:
        # Use your existing database URL from settings
        engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))
        current_db = settings.POSTGRES_DB
        
        with Session(engine) as session:
            # Test connection
            print("\nDatabases:")
            databases = session.exec(text("SELECT datname FROM pg_database;"))
            for db in databases:
                print(f"- {db[0]}")


            stmt = text("SELECT current_database();")
            result = session.exec(stmt)
            db_name = result.first()[0]
            print(f"Successfully connected to database: {db_name}")
            # Get list of databases
                        
            # Version check
            stmt = text("SELECT version();")
            result = session.exec(stmt)
            version = result.first()[0]
            print(f"PostgreSQL version: {version}")
            
            # Get list of tables in the current database
            print(f"\nTables in current database:")
            query = text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """)
            tables = session.exec(query)
            
            table_list = list(tables)
            if not table_list:
                print("No tables found in the database. The database might be empty.")
            else:
                for table in table_list:
                    print(f"- {table[0]}")
                    
                    # Get table columns
                    column_query = text("""
                        SELECT column_name, data_type 
                        FROM information_schema.columns 
                        WHERE table_name = :table_name
                    """)
                    columns = session.exec(column_query, params={"table_name": table[0]})
                    for col in columns:
                        print(f"  • {col[0]}: {col[1]}")
            
    except Exception as e:
        print("Error connecting to the database:")
        print(e)

if __name__ == "__main__":
    test_db_connection()
