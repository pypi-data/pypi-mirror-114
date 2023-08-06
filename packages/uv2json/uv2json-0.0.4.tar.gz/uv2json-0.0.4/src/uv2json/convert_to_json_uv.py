from json import dump
from argparse import ArgumentParser
from pandas import read_csv
from io import StringIO


def convert(filenames):
    """convert files from csv to json

    Args:
        filenames (List[str]): list of filenames with path. each path must be a string
    """
    for filename in filenames:
        # split the file based on dashes; use two dashes since negative numbers also contain dashes
        with open(filename, "r") as infile:
            data = list(filter(None, infile.read().split("--")))  # remove all empty splits
            data = list(
                filter(lambda x: x != "\t", data)
            )  # remove all splits with only tabs ("\t")

        sample_info = list(
            filter(None, data[1].strip("$").split("\n"))
        )  # second item in list contains sample information

        # assemble the dictionary
        sample_dict = {}
        for item in sample_info:
            intensity = item.strip("$").split(":", 1)
            sample_dict[intensity[0]] = intensity[1]

        # read the last item of the data list as a dataframe
        df = read_csv(StringIO(data[-1]), delimiter="\t", names=["254", "280", "320", "FC"])
        # expected format for each column is one of the following:
        # <intensity,time> or <intensity>

        # print(df.info())
        # if <intensity>
        sample_dict["time"] = [i / 10 for i in range(0, df.shape[0])]

        # Kept just in case
        # sample_dict["time"] = [round(float(x.split(",")[1]) * 60, 1) for x in df["254"].to_list()]
        # get time from splitting one column of dataframe and taking the second value in each cell then multiply it by 60 to convert it to seconds
        # TODO: change to just using the first if since it should always be that

        sample_dict["intensities"] = {}  # initialize intensities

        if df.dtypes[0] == "float64":
            for col in df.columns:
                sample_dict["intensities"][col] = [float(x) for x in df[col].to_list()]
        else:
            for col in df.columns:
                sample_dict["intensities"][col] = [
                    float(x.split(",")[0]) for x in df[col].to_list()
                ]

        # write to a json file
        with open(filename.replace(".csv", ".json"), "w") as outfile:
            dump(sample_dict, outfile)


if __name__ == "__main__":
    parser = ArgumentParser(description="Convert Gilson CSV to JSON file")
    parser.add_argument(
        "filenames",
        help="convert given filename(s) to json",
        nargs="+",
    )

    args = parser.parse_args()

    convert(args.filenames)