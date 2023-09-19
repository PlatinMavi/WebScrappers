
chapter_data_list = [[{"manga":"baban"},{"manga":"anan"}]]

new_chapter_documents = []

for chapter_data_unwrapped in chapter_data_list:
    target = chapter_data_unwrapped[0]["manga"]
    # obId = mangas.find_one({"browser":target})["_id"]
    print(target)

    # for chapter_data in chapter_data_unwrapped:
    #     chapter_data["manga"] = obId
    #     fansub_number_tuple = (chapter_data["fansub"], chapter_data["number"], chapter_data["manga"])
    #     if fansub_number_tuple not in unique_field_values:
    #         new_chapter_documents.append(chapter_data)
    #         unique_field_values.add(fansub_number_tuple)  # Update the set