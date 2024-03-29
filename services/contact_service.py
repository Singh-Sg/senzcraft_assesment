
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

# Import necessary modules
from sqlalchemy.exc import IntegrityError
from sqlalchemy import text
import logging
from flask import jsonify
from sqlalchemy.orm import sessionmaker
from models import Contact_Details, Intrest_Table, Base
from db import engine
import tabula

# Define Session and create tables
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)
logging.basicConfig(filename='app.log', level=logging.ERROR)


def store_contact_details(session, row):
    """
    Store data in Contact_Details table.
    """
    # Unpack row data
    sl_no, phone, Contact_First_Name, Contact_Last_Name, Contact_Designation, Contact_eMail = row
    try:
        # Attempt to insert data into Contact_Details table
        session.execute(text("""
            INSERT INTO Contact_Details (Sl_NO, phone, Contact_First_Name, Contact_Last_Name, Contact_Designation, Contact_eMail)
            VALUES (:sl_no, :phone, :Contact_First_Name, :Contact_Last_Name, :Contact_Designation, :Contact_eMail)
        """), {
            'sl_no': int(sl_no),
            'phone': str(phone),
            'Contact_First_Name': str(Contact_First_Name),
            'Contact_Last_Name': str(Contact_Last_Name),
            'Contact_Designation': str(Contact_Designation),
            'Contact_eMail': str(Contact_eMail)
        })
        session.commit()  # Commit transaction
    except IntegrityError:
        # If IntegrityError occurs, try to update existing entry
        session.rollback()  # Rollback transaction
        try:
            session.execute(text("""
                UPDATE Contact_Details
                SET phone = :phone,
                    Contact_First_Name = :Contact_First_Name,
                    Contact_Last_Name = :Contact_Last_Name,
                    Contact_Designation = :Contact_Designation,
                    Contact_eMail = :Contact_eMail
                WHERE Sl_NO = :sl_no
            """), {
                'sl_no': int(sl_no),
                'phone': str(phone),
                'Contact_First_Name': str(Contact_First_Name),
                'Contact_Last_Name': str(Contact_Last_Name),
                'Contact_Designation': str(Contact_Designation),
                'Contact_eMail': str(Contact_eMail)
            })
            session.commit()  # Commit transaction
        except Exception as e:
            session.rollback()  # Rollback transaction
            logging.error(f"An error occurred while updating data in Contact_Details: {str(e)}")
            raise e
    except Exception as e:
        session.rollback()  # Rollback transaction
        logging.error(f"An error occurred while storing data in Contact_Details: {str(e)}")
        raise e
    

def store_interest_table(session, row):
    """
    Store data in Interest_table.
    """
    # Unpack row data
    Id, sl_no, Interest = row
    try:
        # Attempt to insert data into Intrest_Table
        session.execute(text("""
            INSERT INTO Intrest_Table (Id, Sl_NO, Interest)
            VALUES (:Id, :sl_no, :Interest)
        """), 
        {
            'Id': int(Id),
            'sl_no': int(sl_no),
            'Interest': str(Interest)
        }
        )
    except IntegrityError:
        # If IntegrityError occurs, try to update existing entry
        session.rollback()  # Rollback transaction
        try:
            session.execute(text("""
                UPDATE Intrest_Table
                SET Interest = :Interest
                WHERE Id = :Id AND Sl_NO = :sl_no
            """),{
                'Id': int(Id),
                'sl_no': int(sl_no),
                'Interest': str(Interest)
            })
            session.commit()  # Commit transaction
        except Exception as e:
            session.rollback()  # Rollback transaction
            logging.error(f"An error occurred while updating data in Interest_table: {str(e)}")
            raise e
    except Exception as e:
        session.rollback()  # Rollback transaction
        logging.error(f"An error occurred while storing data in Interest_table: {str(e)}")
        raise e


def extract_table(request):
    """
    Extract data from PDF file and store it in the database.
    """
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    pdf_file = request.files["file"]

    if pdf_file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    tables = tabula.read_pdf(pdf_file, pages="all", multiple_tables=True)
    session = Session()

    try:
        for table in tables:
            rows = table.values.tolist()
            if "Contact eMail" in table.columns:
                for row in rows:
                    store_contact_details(session, row)
            else:
                for row in rows:
                    store_interest_table(session, row)

        session.commit()
        session.close()
        return jsonify({"success": True}), 201
    except Exception as e:
        session.rollback()
        session.close()
        return jsonify({"error":"An error occurred while processing the file"}), 500


def get_contact_by_id(id):
    """
    Retrieve contact details by ID.
    """
    try:
        raw_query = """
            SELECT Contact_Details.Sl_NO,
                   Contact_Details.phone,
                   Contact_Details.Contact_First_Name,
                   Contact_Details.Contact_Last_Name,
                   Contact_Details.Contact_Designation,
                   Contact_Details.Contact_eMail,
                   GROUP_CONCAT(Intrest_Table.Interest, ',') AS Interests
            FROM Contact_Details
            LEFT JOIN Intrest_Table ON Contact_Details.Sl_NO = Intrest_Table.Sl_NO
            WHERE Contact_Details.Sl_NO = :id
            GROUP BY Contact_Details.Sl_NO
        """

        session = Session()
        contact_data = session.execute(text(raw_query), {'id': id})

        row = contact_data.fetchone()
        if not row:
            return jsonify({"error": "Contact not found"}), 404

        contact = {
            "Sl_NO": row[0],
            "phone": row[1],
            "Contact_First_Name": row[2],
            "Contact_Last_Name": row[3],
            "Contact_Designation": row[4],
            "Contact_eMail": row[5],
            "Interest": row[6].split(",") if row[6] else []
        }

        return jsonify(contact), 200
        
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return jsonify({"error": "An error occurred while fetching contact"}), 500


def get_all_contacts():
    """
    Retrieve all contacts from the database.
    """
    try:
        raw_query = """
            SELECT Contact_Details.Sl_NO,
                    Contact_Details.phone,
                    Contact_Details.Contact_First_Name,
                    Contact_Details.Contact_Last_Name,
                    Contact_Details.Contact_Designation,
                    Contact_Details.Contact_eMail,
                    GROUP_CONCAT(Intrest_Table.Interest, ',') AS Interests
                FROM Contact_Details
                LEFT JOIN Intrest_Table ON Contact_Details.Sl_NO = Intrest_Table.Sl_NO
                GROUP BY Contact_Details.Sl_NO
            """

        session = Session()
        contact_data = session.execute(text(raw_query))

        rows = contact_data.fetchall()
        fetched_data = []

        for row in rows:
            fetched_data.append({
                "Sl_NO": row[0],
                "phone": row[1],
                "Contact_First_Name": row[2],
                "Contact_Last_Name": row[3],
                "Contact_Designation": row[4],
                "Contact_eMail": row[5],
                "Interest": row[6].split(",") if row[6] else []
            })

        return jsonify(fetched_data), 200
        
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return jsonify({"error": "An error occurred while fetching contacts"}), 500
