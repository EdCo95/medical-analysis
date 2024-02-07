import argparse
import os

import markdown2
import pdfkit

from assess.models.orchestrator import Orchestrator
from assess.structures.criteria import AssessmentCriteria
from assess.structures.medical_record import MedicalRecord


def convert_markdown_to_pdf(md_string: str, output_path: str):
    html_text = markdown2.markdown(md_string)
    pdfkit.from_string(html_text, output_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert Markdown to PDF.")
    parser.add_argument(
        "--record-path", type=str, help="Path to the patient's medical record"
    )
    parser.add_argument(
        "--criteria",
        type=str,
        help="The criteria against which to assess the patient",
        default="colonoscopy",
    )
    parser.add_argument(
        "--write-loc", type=str, help="Output path for the generated report"
    )

    args = parser.parse_args()

    criteria = AssessmentCriteria.from_spec(args.criteria)
    record = MedicalRecord.from_pdf(args.record_path)
    orchestrator = Orchestrator()
    output = orchestrator.run_pipeline(criteria=criteria, record=record)

    fname = f"{record.get_name().replace(' ', '_')}_Assessment.pdf"

    convert_markdown_to_pdf(
        md_string=output, output_path=os.path.join(args.write_loc, fname)
    )
