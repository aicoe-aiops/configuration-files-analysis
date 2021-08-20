---
title: Configuration file analysis
description: misconfigurations detection by discovering frequently occurring patterns in configuration files
---

Software systems have become more flexible and feature-rich. The configuration file for MySQL has more than 200 configuration entries with different subentries.  As a result, configuring these systems is a complicated task and frequently causes configuration errors. These errors are one of the major underlying causes of modern software system failures [[1](http://cseweb.ucsd.edu/~tixu/papers/csur.pdf)]. In 2017, AT&T’s  911 service went down for 5 hours because of a system configuration change [[2](https://thehill.com/policy/technology/325510-over-12000-callers-couldnt-reach-911-during-att-outage)]. About 12600 unique callers were not able to reach 911 during that period. In another similar incident, Facebook and Instagram went down because of a change that affected facebook’s configuration systems [[3](https://mashable.com/2015/01/27/facebook-tinder-instagram-issues/)]. These critical system failures are ubiquitous - In one empirical study, researchers found that the percentage of system failure caused by configuration errors is higher than the percentage of failure resulting from bugs, 30% and 20% respectively [[4](https://atg.netapp.com/wp-content/uploads/2011/10/sosp11-yin.pdf)]. 

Some of the configuration files are written by experts and customized by users such as RHEL tuned files, while others are completely configured by end-users. When writing configuration files, users usually take existing files and modify them with little knowledge of the system. The non-expert user can then easily introduce errors. Even worse, the original file may already be corrupted, and the errors are propagated further. In a lot of these cases, misconfigurations are detected by manually specified rules. However, this process is tedious and not scalable. In this project, we propose data-driven methods to detect misconfigurations by discovering frequently occurring patterns in configuration files. 

* **[Get Started](get-started.md)**

* **[How to Contribute](contribute.md)**

* **[Project Content](content.md)**

## Contact

This project is maintained as part of the AIOps team in Red Hat’s AI CoE as part of the Office of the CTO. More information can be found at https://www.operate-first.cloud/.
