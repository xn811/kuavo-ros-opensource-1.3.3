//
// Created by lfc on 2021/3/1.
//
#include "csv_reader.hpp"

int main(int argc, char const* argv[]) {
    (void)argc;  // Suppress unused parameter warning
    (void)argv;  // Suppress unused parameter warning
    std::vector<std::vector<double>> datas;
    CsvReader::ReadCsvFile("/sros/avia.csv", datas);
    return 0;
}