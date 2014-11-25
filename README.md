# TMFCoreBuildWar

This repository contains the subrepositories needed to build the
[core module](https://github.com/bassosimone/tmfcore) of
[TellMeFirst (TMF)](http://tellmefirst.polito.it/) and specifically
to obtain a WAR suitable to run on, e.g., Tomcat 7.

## How to clone this repository

Since this repository contains submodules, to clone this you have to
run the following command:

    git clone --recursive https://github.com/bassosimone/tmfcore_build

Otherwise, if you have already cloned, you can fetch the submodules using
the following command:

    git submodule update --init

## Dependencies

We use [maven](http://maven.apache.org/) to build and clean the code,
so you need to install it. This repository also assumes that you use
[Java8](https://jdk8.java.net/). So, you need to install Java8 as well.

On Xubuntu 14.04, you can install all the above packages by running
the following command:

    sudo apt-get install maven openjdk-8-jdk

## How to build and clean the code

Once you have installed all the dependencies, you can build the
code using the following command:

    mvn install

You can instead clean the compiled artifacts using:

    mvn clean

To combine both (recommended to be sure that the compile process
starts from scratch) do:

    mvn clean install

## How this repository is organized

The top-level
[pom.xml](https://github.com/bassosimone/tmfcore_build/blob/master/pom.xml)
file references two modules: `tmfcore` and `tmfcore_war`.

The `tmfcore` module (which is also a git submodule) contains the core
functionality of TMF, that is, the `classify()` API. More information on
this module can be found in the [related git
repository](https://github.com/bassosimone/tmfcore).

The `tmfcore_war` module (which is not a git submodule for simplicity but
may become one in the future) contains the code needed to prepare a
Java [Web application ARchive
(WAR)](https://en.wikipedia.org/wiki/WAR_%28file_format%29) that can be
run inside a container, e.g., Tomcat 7.
