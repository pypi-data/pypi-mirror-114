from pyspark.shell import spark

from encoder import Encoder


def main(dataset_path: str = "./data/show_ratings.csv") -> None:
    df = Encoder.prepare_df(spark.read.csv(dataset_path, header=True))

    encoded_df = Encoder.encode(df)
    encoded_df.show()
    df_distance = Encoder.find_max_difference(df)
    df_distance.show()
    df_avg_rating = Encoder.find_avg_rating(df, 8.0)
    df_avg_rating.show()


if __name__ == '__main__':
    main()
