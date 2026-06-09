import os

PDF_FOLDER = "pdfs"

os.makedirs(PDF_FOLDER, exist_ok=True)


def save_uploaded_pdfs(uploaded_files):

    for uploaded_file in uploaded_files:

        file_path = os.path.join(
            PDF_FOLDER,
            uploaded_file.name
        )

        if not os.path.exists(file_path):

            with open(file_path, "wb") as f:

                f.write(uploaded_file.read())


def get_all_pdfs():

    return [
        file
        for file in os.listdir(PDF_FOLDER)
        if file.endswith(".pdf")
    ]


def delete_pdf(filename):

    file_path = os.path.join(
        PDF_FOLDER,
        filename
    )

    if os.path.exists(file_path):

        os.remove(file_path)