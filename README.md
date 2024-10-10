# UPDATE

I put this project on shelf (indefinitely) as of now.

After setting up the Docker instance to scrape the visitor data, my IP got banned after 3 days. And in the meanwhile another group of people applied an almost identical data pipeline, basically implemening everything I've intended to do. 

Doesn't make sense to continue working on a dublicate, time to move on to a new project. I am making one last commit, so that everything I have done, along with the limited data I've gathered is public and accessible to anyone.

# README

Welcome to the `rwth_gym_stats` repository!

## Description

It all started as a joke...

Me and my former flatmate Tobias were taking about how nice it would be to know then the RWTH University gym is usually free. The gym only shares how many people are currently there, and nothing else. Then this project's idea has been incepted.

This repository contains the code for analyzing gym attendance related statistics at RWTH Aachen University's fitness facilities. It aims to provide insights into gym usage patterns, as it remains unknown to the public at the moment.

## Features

- Data collection: The code in this repository collects gym usage data from the official liveticker website, and it is stored internally.
- Containerization: The code runs in a container indefinitely unless interrupted by user for continuous data acquisition.
- (Upcoming) Data analysis: The collected data is analyzed to generate statistics and visualizations.

## Getting Started

To get started with this project, follow these steps:

1. Clone the repository: `git clone https://github.com/dorukresmi/rwth_gym_stats.git`
2. Install the required dependencies: `pip install -r requirements.txt`
3. Run the data collection script: `python main.py`
4. (Upcoming) Visualize the data

## Contributing

Contributions are welcome! If you would like to contribute to this project, please follow these guidelines:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them.
4. Push your changes to your forked repository.
5. Submit a pull request.

Also further functionality suggestions are welcome

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
