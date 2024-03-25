# Trend Score Processor

This application processes time-series data from a CSV file, applies a trend scoring algorithm, and outputs the results to a new CSV file. The process involves normalization and smoothing of weekly interest level changes to produce trend scores ranging from 0 to 100.

## Script

The script is a modified version of the jupyter notebook code. The script performs several key functions:

1. **Data Loading**: It starts by loading the input CSV file specified by the user. This file should contain columns for `company_id`, `topic_id`, `week`, and `interest_level` (It can contain other columns too).

2. **Data Integrity Checks**: To ensure the quality and consistency of the input data, the script uses assertions to validate:
   - Each `topic_id` maps to only one `category_id`.
   - Each `company_id` maps to only one `industry_id`.
   - There are no missing values in critical columns such as `interest_level` and `week`.
   - The `interest_level` values fall within the expected range (0 to 100).
   These checks are crucial for preventing errors during the data processing phase and ensuring that the results are reliable.

3. **Data Processing**:
   - Fills in missing weeks for each `company_id`, `topic_id` pair with zeroes to maintain consistency in the time series.
   - Calculates the weekly change in interest levels.
   - Applies Exponentially Weighted Moving Average (EWMA) smoothing to the weekly changes to identify trends.
   - Removes the filled missing weeks values (This can be changed according to the task).
   - Normalizes these trends into scores ranging from 0 to 100, based on the criteria that scores below 50 indicate a decreasing trend, and scores above 50 indicate an increasing trend.

4. **Output Generation**: Finally, the script outputs the processed data with trend scores to a new CSV file at the specified output path.

### Future Improvements

While the current implementation serves the fundamental requirements of trend scoring, there are several areas where the script could be enhanced in future versions:

1. **Dynamic Parameter Tuning**: Introduce command-line arguments or a configuration file to allow users to adjust parameters such as the EWMA `halflife` or `span` without modifying the script. This flexibility would enable users to tailor the analysis to their specific needs more easily.

2. **Parallel Processing**: For large datasets, the script could leverage parallel processing techniques to improve performance. This might involve using libraries such as Dask to distribute the workload across multiple cores or even multiple machines.

3. **Using Different Library**: Right now, the script uses Pandas for data processing, however the script can be rewritten in Polars or Numpy for higher efficiency.

4. **Enhanced Logging**: While print statements currently provide basic logging functionality, integrating a more sophisticated logging framework would offer greater control over logging levels and outputs. This improvement would facilitate debugging and monitoring the script's execution in production environments.

5. **Feature Handling**: Give user different options for handling other columns not needed for the algorithm.

## Getting Started

These instructions will cover the usage of the Docker application including building the Docker image and running the container to process your data.

### Prerequisites

- Docker installed on your machine. Visit the [official Docker documentation](https://docs.docker.com/get-docker/) to get Docker for your specific operating system.

### Building the Docker Image

1. Clone or download this repository to your local machine.
2. Navigate to the directory containing the Dockerfile and your scripts.
3. Build the Docker image with the following command, replacing `trendscore-processor` with your preferred image name:

    ```bash
    docker build -t trendscore-processor .
    ```

This command reads the Dockerfile in the current directory and builds an image named `trendscore-processor`.

### Processing Data with the Docker Container

To process your CSV file, run the Docker container with the paths to your input and output files as arguments. Ensure these paths are accessible to the Docker container by mounting the directories containing your files.

#### Example Command

To process `folder_one/input.csv` and save the output to `folder_two/output.csv`, use the following command format:

```bash
docker run -v /absolute/path/to/folder_one:/data -v /absolute/path/to/folder_two:/output trendscore-processor /data/input.csv /output/output.csv
```

To process multiple input files, for example: `folder_one/input.csv` and `folder_two/input.csv` using the same image, we need to run multiple docker run commands. Make sure that the output paths of the commands are different, otherwise the data may be overwritten.

### Troubleshooting

If you encounter any issues while running the Docker container, here are a few things you can try:

1. Check the Docker logs for any error messages. You can do this by running the command `docker logs <container_id>`, replacing `<container_id>` with the ID of your Docker container.

2. Ensure that the paths to your input and output files are correct and that they are accessible to the Docker container.

3. Make sure that your Docker image was built successfully. If not, you may need to rebuild it.
