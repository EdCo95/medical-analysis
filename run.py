from assess.structures.medical_record import MedicalRecord

path = "tests/data/non_matching_medical_record.pdf"
# path = "tests/data/medical-record-3.pdf"
record = MedicalRecord.from_pdf(path)
print(record.extract_and_validate_cpt_codes())
