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

    mvn package

You can instead clean the compiled artifacts using:

    mvn clean

To combine both (recommended to be sure that the compile process
starts from scratch) do:

    mvn clean package

## How this repository is organized

The top-level
[pom.xml](https://github.com/bassosimone/tmfcore_build/blob/master/pom.xml)
file references three modules: `tmfcore`, `tmfcore_jaxrs` and `tmfcore_war`.

The `tmfcore` module (which is also a git submodule) contains the core
functionality of TMF, that is, the `classify()` API. More information on
this module can be found in the [related git
repository](https://github.com/bassosimone/tmfcore).

The `tmfcore_jaxrs` module (which is not a git submodule for simplicity but
may become one in the future) contains a Jax-rs annotated Java class that
can be used to generate a RESTful web service exposing TMF's core.

The `tmfcore_war` module (which is not a git submodule for simplicity but
may become one in the future) contains the code needed to prepare a
Java [Web application ARchive
(WAR)](https://en.wikipedia.org/wiki/WAR_%28file_format%29) that can be
run inside a container, e.g., Tomcat 7.

## How to test this code

The web application constructed using `mvn clean package` is located
at `tmfcore_war/target/tmfcore.war`. It assumes that the configuration
file and the indexes are located under `/var/local/tmfcore`.

To populate `/var/local/tmfcore` you need to run the sequence of
commands described next. To avoid running too many commands as root, we
start by creating `/var/local/tmfcore` and assigning it to ourself:

    $ cd /var/local
    $ sudo install -d tmfcore
    $ sudo chown $USER tmfcore

Next we enter into `tmfcore`, we set a reasonable umask, and we
create the required files and directories:

    $ cd tmfcore
    $ umask 022
    $ install -d conf
    $ install -m 644 /dev/null conf/server.properties
    $ git clone https://github.com/TellMeFirst/test-indexes data

Finally, you need to edit `conf/server.properties` to make sure
that it contains the following content:

    corpus.index.it = /var/local/tmfcore/data/index
    kb.it = /var/local/tmfcore/data/index
    residualkb.it = /var/local/tmfcore/data/index
    stopWords.it = /var/local/tmfcore/data/stopwords.it.list

    corpus.index.en = /var/local/tmfcore/data/index
    kb.en = /var/local/tmfcore/data/index
    residualkb.en = /var/local/tmfcore/data/index
    stopWords.en = /var/local/tmfcore/data/stopwords.en.list

### Run the WAR using jetty-runner

We download `jetty-runner` and we also verify the public key:

    $ cd /path/to/tmfcore_build_war
    $ wget http://central.maven.org/maven2/org/eclipse/jetty/jetty-runner/9.2.5.v20141112/jetty-runner-9.2.5.v20141112.jar
    $ wget http://central.maven.org/maven2/org/eclipse/jetty/jetty-runner/9.2.5.v20141112/jetty-runner-9.2.5.v20141112.jar.asc
    $ gpg --recv-keys D7C58886
    $ gpg --verify jetty-runner-9.2.5.v20141112.jar.asc

Next, use `jetty-runner` to run `tmfcore.war` (be patient because it
may take several seconds for `jetty-runner` to be up and running):

    $ java -jar jetty-runner-9.2.5.v20141112.jar \
        tmfcore_war/target/tmfcore.war

Finally, you can run a simple test and check whether it returns a JSON:

    $ ./test/input-jetty.sh

### Run the WAR using Tomcat

You need to have Tomcat 8 installed and you need to make sure that this
instance of Tomcat is run by Java 8.

Go in the `/manager/html` interface of Tomcat and deploy the WAR file.

To test that everything is fine, use the Tomcat-related simple test:

    $ ./test/input-tomcat.sh
