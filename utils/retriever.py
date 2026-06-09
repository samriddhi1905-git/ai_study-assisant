def retrieve_chunks(
    vectordb,
    query,
    selected_pdf=None
):

    if selected_pdf == "All":

        results = vectordb.similarity_search(
            query,
            k=3
        )

    else:

        results = vectordb.similarity_search(
            query,
            k=3,
            filter={
                "filename": selected_pdf
            }
        )

    return results