from reader_generator import ReaderGenerator
# import ex_reader_obj

if __name__ == "__main__":
    readerGenerator = ReaderGenerator()
    readerGenerator.generate_online_reader()

    # exReader = ex_reader_obj.ExReader()
    # exReader.build_files(file_number=exReader.file_number_setting,
    #                      page_start=exReader.page_start_setting,
    #                      page_end=exReader.page_end_setting)
    # exReader.remove_source()