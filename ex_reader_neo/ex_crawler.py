from reader_generator import ReaderGenerator
# import ex_crawler_obj

if __name__ == "__main__":
    readerGenerator = ReaderGenerator()
    readerGenerator.generate_offline_reader()
    
    # ex_crawler = ex_crawler_obj.ExCrawler()
    # [start, end] = ex_crawler.start_end()
    # ex_crawler.build_html(start, end)
    # ex_crawler.remove_source(start)
