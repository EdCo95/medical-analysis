# medical-analysis
Analyses medical records to assess the recommended treatment for each patient.

## Purpose
The goal of this project was to build a system which could analyse patient medical records against the assessment criteria for a colonoscopy and draw a conclusion about whether the patient was eligible for a colonoscopy.

## Approach
The system will undertake this analysis in several steps:
1. **CPT Codes** - the system first extracts the CPT codes for the recommended procedure from the medical record.
2. **CPT Check** - the system performs a web search for the extracted CPT codes, then compares the results against the treatment the doctor has described. This checks for mistakes and confirms that the CPT codes match what the doctor recommended.
3. **Previous Treatment Check** - the system analyses what previous treatment the patient has received and whether any of this has been successful. If so, it returns that the patient is ineligible because previous treatment has helped and should be continued.
4. **Criteria Assessment** - if previous treatment did not help, the system performs a detailed analysis of the colonoscopy criteria against the medical record. It works section-by-section before producing a final analysis.
5. **Writing Results** - the system records each step of the process, forms all of its observations and evidence into a Markdown string, then writes this as a PDF file with its decision and detailed justifications.

## Design Decision Justification
**Efficiency vs Depth of Analysis** The system makes many calls to LLMs to undertake this analysis. Due to the critical nature of the task, given that it relates to healthcare, I elected to trade efficiency for depth of analysis. By making many calls to the LLMs, the system ensures the highest possible chance of a correct analysis due to the ensembling effect. The calls to the LLMs could be streamlined with further automated testing in place to monitor performance.

**Usage** The system is run as a command line tool. It ingests PDFs and outputs PDFs. I elected to build it this way so that the resulting PDFs could be directly interpreted by medical professionals who are likely more familiar with the PDF format than the Markdown format. The system could be deployed as a web app instead and paired with a front end - doing so would require minimal changes.

## Notable Features
* **Testing** - there is a suite of unit and integration tests. Run with `make test` or `pytest tests`.
* **Retrying** - one of the utility functions can be used as a decorator (`@retry_on_failure(tolerance=3)`). This decorator can be added to any function which calls an LLM to add a small tolerance for failures or timeouts.
* **LLMs as Test Assessors** - one of the challenges with automatically testing large language models is the variability of their outputs. One of the tests (`intergration_tests/test_medical_record_object.py/test_that_it_can_present_evidence_treatment_helped()`) demonstrates how LLMs can be used to test their own outputs.
* **Markdown and PDF Formatting** - the system can output its analysis as a PDF file, Markdown file, or can return simple boolean indicators for acceptance / rejection.
* **Any Criteria** - the system is not hard coded to assess patients for colonoscopy. You can add any criteria you like in `assess/models/criteria` and then specify it for use in the pipeline. As long as the criteria you add is in the same logical format as the colonoscopy example, the system will assess against it, making it easy to extend the system with any assessment criteria you like.
* **Dev Tools** - the project automatically lints and formats code on commit using the `black`, `isort`, `flake8`, and `pre-commit` libraries, helping to maintain code standards and prevent styling debates between developers.

## Future Improvements
Given the fast nature of the project, there are several important features that should be added in future:
* **Testing** - automated tests that LLM endpoints are live should be added along with more much more extensive unit and integration testing with more example records to measure performance.
* **Council of Advisors** - integration with multiple LLMs (e.g. Anthropic) to provide a "Council of Advisors" rather than just a single LLM. The code is designed with this in mind - as long as the objects implement the interfaces shown, they can be used interchangeably.
* **Current Date** - the LLM needs to be informed of the current date so that it can accurately assess how long it has been since certain procedures.
* **Verification of Quoted Evidence** - the LLM quotes evidence for each step of the pipeline. Verification that these quotes came from the medical record and criteria should be added to ensure there are no hallucinations.
* **Improved Formatting** - the final PDF output's formatting is basic and could be improved to add readability.
* **Exponential Backoff In Retries** - when retrying LLM calls on failure, the decorator could include exponential backoff rather than instantly retrying.
* **DevOps Pipeline** - an automated pipeline to run the tests and build the docker image should be added.

## Installing and Running
In order to generate PDFs, the non-Python package `wkhtmltopdf` is required. For convenience, a Dockerfile has been provided which installs this and all necessary dependencies. Additionally, a Makefile is provided to give shortcuts for the various commands.

### Installation
To use the Makefile, you will need to have `make` installed. On Ubuntu do so with:
```commandline
sudo apt-get install make
```
On MacOS, use Homebrew:
```commandline
brew install make
```
Check your installation with:
```commandline
make -version
GNU Make 4.4.1
Built for x86_64-apple-darwin22.3.0
Copyright (C) 1988-2023 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <https://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
```
Once `make` is installed, to install this project simply run:
```commandline
make install-dev
```
`make install-dev` will create a virtual environment, install all dependencies, and install `pre-commit`. If you do not wish to install `pre-commit`, run `make install-deploy` instead.

### Using Docker
If you have `make` installed, use the convenience command provided in the Makefile to build the docker image:
```commandline
make docker-build
```

If you'd prefer not to use `make`, instead run:
```commandline
docker build -t medical-assessment .
```

To run the code, **it is strongly recommended to use Docker**. This will mean you do not need to install `wkhtmltopdf` manually because it will be installed in the docker container. In order to do so, you must first export your OpenAI API key with access to GPT-4 in your environment:
```commandline
export OPENAI_API_KEY="sk-..."
```

Once you have exported your API key and built the docker image, you can run the code using the convenience command in the Makefile:
```commandline
make analyse RECORD_PATH="tests/data/medical-record-1.pdf" WRITE_LOC="./"
```

Replace RECORD_PATH with the path to the medical record PDF you wish to use. By default, the system will assess against the criteria for a colonoscopy. The system will write the resulting PDF to a file with the patient's name followed by "_Assessment.pdf". Some examples can be seen in the `examples/` directory.

To run the system without make:
```commandline
docker run -e OPENAI_API_KEY=$OPENAI_API_KEY -v $(PWD):/app medical-assessment --record-path /app/tests/data/medical-record-1.pdf --write-loc /app/./
```

This will inject your API key into the container and mount your local directory into it to write the results.

To run without docker:
```commandline
python run.py --record-path tests/data/medical-record-1.pdf --write-loc ./
```

Additionally, you can specify a different criteria with:
```commandline
python run.py --record-path tests/data/medical-record-1.pdf --criteria YOUR_CRITERIA_NAME --write-loc ./
```

Remember, to run with a different criteria, you will need to place it in the `src/assess/models/criteria` directory, and it will need to be in the same logical format as `colonoscopy.toml`. Also, to run without docker, you must have `wkhtmltopdf` installed.
