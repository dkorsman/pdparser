# pdparser 

_A Tool for Analysing Higher-Order Feature Interactions in Preprocessor Annotations in C and C++ Projects_

## Abstract

Feature interactions are an intricate phenomenon: they can add value to software systems, but also lead to subtle bugs and complex, emergent behavior.
Having a clearer understanding of feature interactions in practice can help practitioners to select appropriate quality assurance techniques for their systems and researchers to guide further research efforts.
In this repository, you find **pdparser**, a Python-based tool for analyzing structural feature interactions in software systems developed with C and C++ preprocessor.
pdparser relies on a lightweight methodology to quantify the frequency of pairwise and higher-order feature interactions and the percentage of code affected by them.

## Tool Description

On a high level, the methodology used in pdparser consists of parsing the C/C++ source files of a project, extracting preprocessor directives within these files, and reasoning about these directives. 
This tool is designed purely based on **parsing preprocessors directives** rather than writing or extending a full C or C++ parser or compiler. 
Users have access to the following functionalities: 

1. Analyze all source code files in a C/C++ project
2. Analyze projects in batch mode
3. Export the results in JSON format
4. Visualize the variability information
5. Check occurrence of features in multiple projects
6. Test project for getting started

## Getting started

The tool can be executed using the file **pdparser.py** via command line interface (CLI).
There is a help menu which can be accessed via CLI using the command ``pdparser.py -h``. 

```
 usage: pdparser.py [-h] [-o OUTPUT] [-q [CAT [CAT ...]]] [-d] [-f] [-B] [-jr]
                   [-jp] [-u UNIQUE_FEATURE_FILTER]
                   source
   -o, --output          the source folder to operate on
   -q, --quiet           silence a category of messages
   -d, --hide-code       hide code from output files except 
                         preprocessor directives and annotations
   -f, --features        try to get all involved features in defined(X)
   -B, --no-blacklist    ignore pdparser-blacklist.lst file 
                         (to get all files again)
   -jr, --json-result    store a json file with general results in 
                         the output folder
   -jp, --json-pinpoint  store json files with all locations of nesting levels
                         and feature interactions
   -u UNIQUE_FEATURE_FILTER, --unique-feature-filter UNIQUE_FEATURE_FILTER
                         the count-project-features.json to use for filtering
                         UNIQUE features - pass only if you want to filter
```

### Demo video

In the wiki, there is a [demo video](https://github.com/dkorsman/pdparser/wiki/Demonstration-video) showing how to use the tool.
The video can also be watched on [youtube](https://www.youtube.com/watch?v=vrXnQ-hzkYE).
[![pdparser demo video](https://img.youtube.com/vi/vrXnQ-hzkYE/0.jpg)](https://www.youtube.com/watch?v=vrXnQ-hzkYE "pdparser - demo video")

## Information

For more information, feel free to contact the authors or use the issues/pull request menu.

### David Korsman
Email: <david.korsman@ru.nl>

### Carlos Diego N. Damasceno
Email: <damasceno.diego [at] gmail.com> 
Website: http://damascenodiego.github.io

### Daniel Strüber
Email: <danstru [at] chalmers.se>
Website: https://www.danielstrueber.de/
