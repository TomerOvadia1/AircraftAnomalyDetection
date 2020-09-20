import logging
import pandas as pd
import csv
import utils


class DataCleaner:
    def __init__(self, file_name, output_directory):
        self._log = utils.get_logger(self.__class__.__name__)
        self._file_name = file_name
        self._output_dir = output_directory

    def execute_labeld(self):
        self._log.info(f"Started DataCleaner for file {self._file_name}")
        with open(self._file_name, "r") as f:
            reader = csv.reader(f, delimiter=",")
            lines = []
            command_fault = ""
            command = ""
            for i, line in enumerate(reader):
                if i == 0:
                    line.pop()
                    line.append("Command_fault")
                    line.append("Command")
                    lines.append(line)
                    continue

                if line[0].startswith("Command_Fault"):
                    command_fault = line[0].split(":")[1]
                elif line[0].startswith("Command:"):
                    command = line[0].split(":")[1]
                else:
                    line.pop()
                    line.append(command_fault)
                    line.append(command)
                    lines.append(line)
        new_file_name = self._output_dir + "\\" + "cleaned_" + self._file_name.split("\\")[-1]
        with open(new_file_name, "w+", newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            for line in lines:
                writer.writerow(line)

    def execute_non_labled(self):
        self._log.info(f"Started DataCleaner for file {self._file_name}")
        with open(self._file_name, "r") as f:
            reader = csv.reader(f, delimiter=",")
            lines = []
            for _, line in enumerate(reader):
                if line[0].startswith("Command_Fault") or line[0].startswith("Command:"):
                    continue
                else:
                    line.pop()
                    lines.append(line)
        new_file_name = self._output_dir + "\\" + "cleaned_" + self._file_name.split("\\")[-1]
        with open(new_file_name, "w+", newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            for line in lines:
                writer.writerow(line)

if __name__ == "__main__":
    csvs_found = utils.get_all_csv_files(
        "C:\\Users\Tomer\Desktop\\University\\3rd\Anomaly detection\Project\\original_data\\set5")
    for file in csvs_found:
        DataCleaner(
            file_name=file,
            output_directory="C:\\Users\\Tomer\\Desktop\\University\\3rd\\Anomaly detection\\Project\\cleaned_data\\non_labeld\\set5"
        ).execute_non_labled()

        DataCleaner(
            file_name=file,
            output_directory="C:\\Users\\Tomer\\Desktop\\University\\3rd\\Anomaly detection\\Project\\cleaned_data\\labeld\\set5"
        ).execute_labeld()
