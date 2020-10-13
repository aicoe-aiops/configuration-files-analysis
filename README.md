# Configuration file analysis

## Overview

Software systems have become more flexible and feature-rich. For example, the configuration file for MySQL has more than 200 configuration entries with different subentries.  As a result, configuring these systems is a complicated task and frequently causes configuration errors. Currently, in most cases, misconfigurations are detected by manually specified rules. However, this process is tedious and not scalable. In this project, we propose data-driven methods to detect misconfigurations by discovering frequently occurring patterns in configuration files. 

## Misconfiguration detection framework

The misconfiguration detection framework adopted in this project is inspired by the research paper "Synthesizing Configuration File Specifications with Association Rule Learning". Association rule learning is a method to discover frequently occurring patterns or associations between variables in a dataset. 

![image alt text](notebooks/images/framework.png)Figure 1: Overview of the misconfiguration detection framework. It has two important modules: translator and learner. 

* Translator: Translator works as a parser, translator converts raw configuration files into an intermediate representation which generally has a format of key, value, data type, frequency (k, v, τ, f)

* Learner: Learner discovers frequently occurring patterns or associations between keywords in configuration files to derive rules.

Data type error detection:  In this method, we match the data type of target key with the data type information inferred from the training set. An error is reported if the matching fails.

Spelling error detection: In this method, we find spelling errors by mapping lower frequency keywords to a similar higher frequency keyword. We calculated the similarity between keywords using Levenshtein distance. 

## Project organization

------------

    ├── src                

    │   ├── data

    │   │   └── data_downloader.py  <- Script to download the configuration file dataset

    ├── notebooks          

    |	└── Misconfiguration_detection_framework_for_data_type_errors.ipynb <- notebook for data type error detection in configuration files.
    	└── Misconfiguration_detection_framework_for_spelling_errors.ipynb <- notebook for spelling error detection in configuration files.

## Conclusion

In this project, we discovered frequently occurring patterns in MySQL configuration files to detect misconfiguration. We experimented with two types of errors based on patterns in configuration files.  We detected data type errors by matching the target key data type with the data type information inferred from the training set. We detected spelling error by mapping lower frequency keyword to a similar higher frequency keyword. We can easily extend this to include other types of errors based on patterns in the configuration files. The results suggest that we can automate the misconfiguration detection task using data-driven methods for all types of key-values based configuration files. 

