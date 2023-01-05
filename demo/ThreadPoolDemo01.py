import concurrent.futures
import time

def process_data(data):
    # 在这里处理数据
    result = data
    time.sleep(2)  # 睡眠 1 秒
    print(f'Processing data {data}')  # 打印输出
    return result

def main():
    # 创建线程池，并设置最大并发线程数为 4
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        # 将循环中的每一项数据提交到线程池中执行
        for i in range(10):
            future = executor.submit(process_data, i)
            # 当线程任务完成时，调用 result() 方法获取结果

if __name__ == '__main__':
    main()
