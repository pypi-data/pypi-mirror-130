import langid
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class Analyzer:
    def __init__(self):
        pass

    @staticmethod
    def get_text_language(text: str):
        return langid.classify(text)[0]

    @staticmethod
    def get_text_string_length(text: str):
        return len(text)

    @staticmethod
    def get_text_token_length(text: str, model_tokenizer=None):
        if not model_tokenizer:
            from transformers import BertTokenizer
            model_tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased')
        return len(model_tokenizer.tokenize(text))

    @staticmethod
    def show_dataframe_base_info(df: pd.DataFrame, column=None):
        if column:
            df = df[column]
        print(df.describe())
        print(df.info())

    @staticmethod
    def show_dataframe_completely():
        """
            完全显示pandas的dataframe的所有值
        Returns:

        """
        import pandas as pd
        pd.set_option('max_colwidth', 500)  # 设置value的显示长度为200，默认为50
        pd.set_option('display.max_columns', None)  # 显示所有列，把行显示设置成最大
        pd.set_option('display.max_rows', None)  # 显示所有行，把列显示设置成最大

    @staticmethod
    def show_plt_completely():
        """
            plt显示问题
        Returns:

        """
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

    @staticmethod
    def analyze_numerical_array(data):
        """
        分析数值数组
        Args:
            data:

        Returns:

        """
        Analyzer.show_plt_completely()
        if not isinstance(data, np.ndarray):
            data = np.array(data)

        q1 = np.percentile(data, 25)  # 第一四分位数，从小到大25%,下四分位数
        q2 = np.percentile(data, 50)  # 第二四分位数，从小到大50%，中位数
        q3 = np.percentile(data, 75)  # 第三四分位数，从小到大75%，上四分位数
        iqr = q3 - q1  # 四分位数差（IQR，interquartile range），上四分位数-下四分位数
        lower_limit = q1 - 1.5 * iqr
        upper_limit = q3 + 1.5 * iqr
        print(f"""
        计数：      {len(data)}
        均值：      {data.mean()}
        标准差：     {data.std()}
        方差：      {data.var()}
        最大值：    {np.max(data)}
        最小值：    {np.min(data)}
        下四分位数： {q1}
        中位数：     {q2}
        上四分位数:  {q3}
        下异常值界限：{lower_limit}   ,异常值数:{len(np.where(data < lower_limit)[0])}
        上异常值界限：{upper_limit}   ,异常值数:{len(np.where(data > upper_limit)[0])}
            """
              )
        plt.subplot(211)
        plt.hist(data)
        plt.subplot(212)
        plt.boxplot(data, vert=False)
        plt.show()

    @staticmethod
    def analyze_category_array(data: pd.Series):
        """
        分析类型数据
        Args:
            data:

        Returns:

        """
        Analyzer.show_plt_completely()
        if not isinstance(data, pd.Series):
            data = pd.Series(data)
        data_value_counts = data.value_counts()
        data_pie = data_value_counts / len(data)
        print(f"""
        data: 
        {data_value_counts}
        data_percent:
        {data_pie.sort_values}
        """
              )
        plt.subplot()
        data_value_counts.plot.bar()
        plt.show()
        plt.subplot()
        data_pie.plot.pie(autopct='%.1f%%', title='pie', )
        plt.show()


if __name__ == '__main__':
    a = pd.Series(['a', 'b', 'd', 'a', 'c', 'd', 'b', 'a', 'c', 'a', 'c'])
    Analyzer.analyze_category_array(data=a)
