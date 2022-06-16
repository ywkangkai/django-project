def get_file_content(filename, chunk_size=1024):
    with open(filename, encoding='utf-8')as f:
        while True:
            content = f.read(chunk_size)
            #如果文件结尾，那么content为None
            if not content:
                break
            yield content


