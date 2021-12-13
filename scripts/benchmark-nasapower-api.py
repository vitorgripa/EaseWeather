from time import time
import requests

OUTPUT_FORMAT = (
    "netcdf",
    "csv",
    "json",
    "ascii",
    "icasa",
    "xarray"
)
url = "http://localhost:8000/?latitude=-22.45&longitude=-45.22&output={output}"

with open("./data/benchmarks/nasapower-api.csv", "w") as benchmark_file:
    benchmark_file.write("N REQ,FORMATO,TEMPO\n")

    for output in OUTPUT_FORMAT:

        for i in range(11):

            output_url = url.format(output=output)

            response = requests.get(output_url)

            tempo = response.content.decode("utf-8")

            linha = f"{i},{output},{tempo}\n"

            benchmark_file.write(linha)

            print(linha)