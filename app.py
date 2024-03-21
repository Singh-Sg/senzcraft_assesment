
from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import tabula

# Initialize Flask app
app = Flask(__name__)

# Create an engine to connect to the SQLite database
engine = create_engine("sqlite:///data.db", echo=True)
Base = declarative_base()

# Define models for the tables
class Contact_Details(Base):
    __tablename__ = "Contact_Details"
    Sl_NO = Column(Integer, primary_key=True)
    phone = Column(String)
    Contact_First_Name = Column(String)
    Contact_Last_Name = Column(String)
    Contact_Designation = Column(String)
    Contact_eMail = Column(String)

class IntrestTable(Base):
    __tablename__ = "Interest_table"
    Id = Column(Integer, primary_key=True)
    Sl_NO = Column(Integer, ForeignKey("Contact_Details.Sl_NO"))
    Interest = Column(String)

# Create the tables in the database
Base.metadata.create_all(engine)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)

# Route to extract table data from PDF file
@app.route("/uploadfile", methods=["POST"])
def extract_table():
    """
    Extract table data from PDF file and update database.

    Accepts a PDF file and updates the Contact_Details and Interest_table
    tables in the database based on the extracted data.
    """
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    pdf_file = request.files["file"]

    if pdf_file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    tables = tabula.read_pdf(pdf_file, pages="all", multiple_tables=True)
    session = Session()

    for table in tables:
        rows = table.values.tolist()
        if "Contact eMail" in table.columns:
            for row in rows:
                (
                    sl_no,
                    phone,
                    Contact_First_Name,
                    Contact_Last_Name,
                    Contact_Designation,
                    Contact_eMail,
                ) = row
                existing_contact = (
                    session.query(Contact_Details).filter_by(Sl_NO=int(sl_no)).first()
                )
                if existing_contact:
                    # Update existing contact
                    existing_contact.phone = str(phone)
                    existing_contact.Contact_First_Name = str(Contact_First_Name)
                    existing_contact.Contact_Last_Name = str(Contact_Last_Name)
                    existing_contact.Contact_Designation = str(Contact_Designation)
                    existing_contact.Contact_eMail = str(Contact_eMail)
                else:
                    # Add new contact
                    data_entry = Contact_Details(
                        Sl_NO=int(sl_no),
                        phone=str(phone),
                        Contact_First_Name=str(Contact_First_Name),
                        Contact_Last_Name=str(Contact_Last_Name),
                        Contact_Designation=str(Contact_Designation),
                        Contact_eMail=str(Contact_eMail),
                    )
                    session.add(data_entry)
        else:
            for row in rows:
                Id, sl_no, Interest = row
                existing_interest = (
                    session.query(IntrestTable).filter_by(Id=int(Id)).first()
                )
                if existing_interest:
                    existing_interest.Interest = str(Interest)
                else:
                    data_entry = IntrestTable(
                        Id=int(Id), Sl_NO=int(sl_no), Interest=str(Interest)
                    )
                    session.add(data_entry)

    session.commit()
    session.close()
    return jsonify({"success": True}), 201

# Route to get all contact data
@app.route("/contact", methods=["GET"])
def get_contacts():
    """
    Get all contact data.

    Fetches all contact data from the Contact_Details table and their
    corresponding interests from the Interest_table table.
    """
    session = Session()
    contacts = session.query(Contact_Details).all()
    interests = session.query(IntrestTable).all()
    session.close()

    contact_dict = {}
    for contact in contacts:
        contact_dict[contact.Sl_NO] = {
            "Sl_NO": contact.Sl_NO,
            "phone": contact.phone,
            "Contact_First_Name": contact.Contact_First_Name,
            "Contact_Last_Name": contact.Contact_Last_Name,
            "Contact_Designation": contact.Contact_Designation,
            "Contact_eMail": contact.Contact_eMail,
            "interests": [],
        }

    for interest in interests:
        if interest.Sl_NO in contact_dict:
            contact_dict[interest.Sl_NO]["interests"].append(interest.Interest)

    contacts_list = list(contact_dict.values())

    return jsonify(contacts_list), 200

# Route to get contact data by ID
@app.route("/contact/<int:id>", methods=["GET"])
def get_contact_id(id):
    """
    Get contact data by ID.

    Fetches contact data from the Contact_Details table and their
    corresponding interests from the Interest_table table based on the
    provided ID.
    """
    session = Session()
    contact = session.query(Contact_Details).filter_by(Sl_NO=id).first()
    interests = session.query(IntrestTable).filter_by(Sl_NO=id).all()

    intr = []
    for interest in interests:
        intr.append(interest.Interest)
    else:
        print("Contact not found")
    if contact:
        data = {
            "Sl_NO": contact.Sl_NO,
            "phone": contact.phone,
            "Contact_First_Name": contact.Contact_First_Name,
            "Contact_Last_Name": contact.Contact_Last_Name,
            "Contact_Designation": contact.Contact_Designation,
            "Contact_eMail": contact.Contact_eMail,
            "interest": intr,
        }
        return (jsonify(data)), 200
    else:
        return jsonify({"error": "Contact not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
