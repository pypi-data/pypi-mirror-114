# Clashgap

[![Version](https://img.shields.io/pypi/v/clashgap?label=version)](https://pypi.org/project/clashgap)
[![Downloads](https://static.pepy.tech/personalized-badge/clashgap?period=month&units=abbreviation&left_color=grey&right_color=blue&left_text=downloads/month)](https://pepy.tech/project/clashgap)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-blue.svg)](http://makeapullrequest.com)
[![Code Quality](https://img.shields.io/lgtm/grade/python/g/NioGreek/Clashgap.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/NioGreek/Clashgap/context:python)
[![Tests Status](https://github.com/NioGreek/Clashgap/actions/workflows/test.yml/badge.svg)](https://github.com/NioGreek/Clashgap/actions)
[![Build Status](https://github.com/NioGreek/Clashgap/actions/workflows/build.yml/badge.svg)](https://github.com/NioGreek/Clashgap/actions)
[![Docs Status](https://readthedocs.org/projects/clashgap/badge/?version=latest)](https://clashgap.readthedocs.io/en/latest/)

A per-character diff/compression algorithm implementation in python

## How it works

In case if you have two strings:
> "This is a sentence..." and "This is a word..."

you could "clash" both of them together and find their gap, to get an array loking something like:
> \["This is a", \["sentence", "word"\], "..."\]

As you can the clashgap algorithm looks for collisions in the two strings to find the gap. The clashgaped string maybe used for compression or as the diff of the input strings
