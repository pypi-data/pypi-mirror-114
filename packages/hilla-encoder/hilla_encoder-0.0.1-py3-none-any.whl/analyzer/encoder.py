from pyspark.ml.feature import StringIndexer
from pyspark.shell import spark
from pyspark.sql import DataFrame, Window
from pyspark.sql.functions import to_date, dayofmonth, month, row_number, avg, lead, desc, datediff, max
from pyspark.sql.types import DoubleType, IntegerType

from global_const_dir import TITLE, DATE, RATING, DATE_DAY_OF_MONTH, DATE_MONTH, RATING_NUMBER, AVERAGE_RATING


class Encoder:

    @staticmethod
    def find_max_difference(df: DataFrame) -> DataFrame:
        df_with_next_date = df.select(
            df[TITLE],
            df[DATE],
            lead(df[DATE], 1).over(
                Window.partitionBy(TITLE).orderBy(desc(DATE))).alias('next_date')
        )
        df_with_difference = df_with_next_date.select(
            df_with_next_date[TITLE],
            datediff(df_with_next_date[DATE], df_with_next_date['next_date']).alias('difference')
        )

        df = df_with_difference.groupBy(TITLE).agg(max('difference').alias('difference'))

        return df

    @staticmethod
    def find_avg_rating(df: DataFrame, rating_threshold: float) -> DataFrame:
        all_titles = df.select(TITLE).distinct()
        filtered_df = df.filter(df.Rating >= rating_threshold).groupby(TITLE).agg(avg(RATING).alias(RATING))
        return filtered_df.join(all_titles, TITLE, 'right').select('*').fillna(0)

    @staticmethod
    def encode(df: DataFrame) -> DataFrame:
        df = Encoder._add_rating_numbers(df)
        df = Encoder._index_identity_column(df)
        df = Encoder._prepare_df_to_flatenning(df)
        avg_chart = Encoder._create_avg_chart(df)
        df = Encoder._flatten_df(df)
        df = df.join(avg_chart, df[TITLE] == avg_chart[TITLE])
        return df

    @staticmethod
    def prepare_df(df: DataFrame) -> DataFrame:
        return df.select(
            df[TITLE],
            to_date(df[DATE], 'MM/dd/yyyy').alias(DATE),
            df[RATING].cast(DoubleType()).alias(RATING),
        )

    @staticmethod
    def _index_identity_column(df: DataFrame) -> DataFrame:
        string_indexer = StringIndexer(inputCol=TITLE, outputCol='Index')
        return string_indexer.fit(df).transform(df)

    @staticmethod
    def _prepare_df_to_flatenning(df: DataFrame) -> DataFrame:
        return df.select(
            df['Index'].alias(TITLE).cast(IntegerType()),
            dayofmonth(df[DATE]).alias(DATE_DAY_OF_MONTH),
            month(df[DATE]).alias(DATE_MONTH),
            df[RATING],
            df[RATING_NUMBER]
        )

    @staticmethod
    def _add_rating_numbers(df: DataFrame) -> DataFrame:
        df_ordered = df.select(df['*']).orderBy(DATE, ascending=True)
        return df_ordered.select(df_ordered['*'],
                                 row_number().over(Window.partitionBy(TITLE).orderBy(DATE)).alias(RATING_NUMBER))

    @staticmethod
    def _flatten_df(df: DataFrame) -> DataFrame:
        query = f"""
            SELECT
                df1.{TITLE} {TITLE},
                df1.{DATE_DAY_OF_MONTH} 1_{DATE_DAY_OF_MONTH},
                df1.{DATE_MONTH} 1_{DATE_MONTH},
                df1.{RATING} 1_{RATING},
                df2.{DATE_DAY_OF_MONTH} 2_{DATE_DAY_OF_MONTH},
                df2.{DATE_MONTH} 2_{DATE_MONTH},
                df2.{RATING} 2_{RATING}
            FROM df1
            LEFT JOIN df2
            ON df1.{TITLE} = df2.{TITLE}
        """
        df1 = df.select(df['*']).where(df[RATING_NUMBER] == 1)
        df2 = df.select(df['*']).where(df[RATING_NUMBER] == 2)
        df1.createTempView('df1')
        df2.createTempView('df2')
        joined_df = spark.sql(query)
        return joined_df

    @staticmethod
    def _create_avg_chart(df: DataFrame) -> DataFrame:
        return df.groupBy(TITLE).agg(avg(RATING).alias(AVERAGE_RATING))
