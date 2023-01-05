class  FileUtil:
    def read_file(self, filepath: str) -> str:
        """读取文件内容并返回"""
        with open(filepath, 'r') as f:
            return f.read()

    def write_file(self, filepath: str, contents: str):
        """将内容写入文件"""
        with open(filepath, 'w') as f:
            f.write(contents)
    def append_file(self,filepath:str,contents:str):
        with open(filepath,'a') as f:
            f.write(contents)

if __name__ == '__main__':
    # 1.使用工具类读取文件
    helper = FileUtil()
    contents: str = helper.read_file('../myfile.txt')
    strList: list[str] = contents.split("\n")
    helper.write_file("outTest.txt", "123")