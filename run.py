from assess.structures.medical_record import MedicalRecord

# path = "tests/data/medical-record-1.pdf"
path = "tests/data/medical-record-3.pdf"
record = MedicalRecord.from_pdf(path)
print(record.present_evidence_treatment_helped())
